"""Grid2Op environment adapter — enhanced implementation.

This adapter wraps Grid2Op environments and exposes a normalized, model-friendly
interface:

- reset() -> observation vector (numpy array)
- step(action) -> (obs_vector, reward, done, info)
- get_topology() -> networkx graph (if available)
- get_obs_dim() -> integer input dimension
- _obs_to_vector(obs) -> numpy array (best-effort conversion)
- _vector_to_action(v) -> grid2op.Action (best-effort, may return None)

Notes on robustness:
- Grid2Op versions differ in their observation/action APIs. This adapter uses a
  defensive strategy: it tries several common methods (to_array/to_vect/to_numpy)
  and falls back to extracting numeric attributes. When a full conversion to a
  grid2op.Action is not possible automatically, _vector_to_action returns None
  and the caller should use env.noop_action() or another safe default.

- For fast local testing we provide a tiny fallback environment that returns
  simple dict observations and supports the same methods.
"""
from .base import Environment
from typing import Tuple, Any
import numpy as np
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Grid2OpEnv(Environment):
    def __init__(self, env_name: str = "l2rpn_neurips_2020", tiny: bool = False):
        self.env_name = env_name
        self.tiny = tiny
        self.env = None
        self._obs_dim = None
        if not self.tiny:
            try:
                import grid2op
                # Prefer factory helpers when present
                if hasattr(grid2op, "make"):
                    self.env = grid2op.make(self.env_name)
                elif hasattr(grid2op, "create_env"):
                    self.env = grid2op.create_env(self.env_name)
                else:
                    # Try older API
                    try:
                        from grid2op.Environment import Environment as G2OEnv
                        self.env = G2OEnv(self.env_name)
                    except Exception:
                        self.env = None
                if self.env is None:
                    raise RuntimeError(
                        "Could not instantiate grid2op environment. Please check your grid2op installation and dataset."
                    )
            except ModuleNotFoundError:
                raise ModuleNotFoundError(
                    "grid2op is not installed in your environment. Install grid2op (pip install grid2op) or run in --tiny mode for a local test."
                )
        else:
            # fallback tiny environment
            self.env = _TinyFallbackEnv()

    def reset(self) -> np.ndarray:
        """Reset underlying env and return a numpy vector observation."""
        raw = None
        if self.tiny:
            raw = self.env.reset()
        else:
            try:
                res = self.env.reset()
                # some versions return the observation directly
                if res is not None:
                    raw = res
                else:
                    # try common accessors
                    if hasattr(self.env, "get_obs"):
                        raw = self.env.get_obs()
                    elif hasattr(self.env, "observation"):
                        raw = self.env.observation
                    elif hasattr(self.env, "last_obs"):
                        raw = self.env.last_obs
                    else:
                        raw = None
            except Exception as e:
                raise RuntimeError(f"Error while resetting grid2op env: {e}")

        vec = self._obs_to_vector(raw)
        # cache obs_dim
        self._obs_dim = int(vec.shape[0]) if vec is not None else None
        return vec

    def step(self, action) -> Tuple[np.ndarray, float, bool, dict]:
        """Apply action (grid2op.Action or a numpy vector). Returns (obs_vec, reward, done, info)."""
        # If action is a numpy vector, try to convert to grid2op.Action
        action_obj = action
        if not self.tiny and action is not None and isinstance(action, (np.ndarray, list, tuple)):
            try:
                action_obj = self._vector_to_action(np.array(action))
            except Exception as e:
                logger.debug(f"_vector_to_action raised: {e}")
                action_obj = None

        if self.tiny:
            obs, reward, done, info = self.env.step(action_obj)
            vec = self._obs_to_vector(obs)
            return vec, reward, done, info

        try:
            res = self.env.step(action_obj)
        except Exception as e:
            raise RuntimeError(f"Error during env.step(action): {e}")

        # Normalize possible return signatures
        obs = None
        reward = None
        done = False
        info = {}
        if isinstance(res, tuple):
            if len(res) == 4:
                obs, reward, done, info = res
            elif len(res) == 3:
                reward, done, info = res
                # try to get latest obs
                if hasattr(self.env, "get_obs"):
                    obs = self.env.get_obs()
                elif hasattr(self.env, "last_obs"):
                    obs = getattr(self.env, "last_obs")
                else:
                    obs = None
            else:
                # unexpected tuple
                obs = None
        else:
            # some APIs return info objects; try to read last_obs
            if hasattr(self.env, "get_obs"):
                obs = self.env.get_obs()
            elif hasattr(self.env, "last_obs"):
                obs = getattr(self.env, "last_obs")

        vec = self._obs_to_vector(obs)
        return vec, reward, done, info

    def get_topology(self):
        try:
            if self.tiny:
                return self.env.get_topology()
            if hasattr(self.env, "get_topology"):
                return self.env.get_topology()
            # some grid2op envs expose a "grid" or "simu" object
            if hasattr(self.env, "grid"):
                return getattr(self.env, "grid")
            return None
        except Exception:
            return None

    def get_observation_space(self):
        # not standardized across versions; return None or best-effort dict
        return None

    def get_action_space(self):
        # best-effort
        if self.tiny:
            return None
        if hasattr(self.env, "action_space"):
            return getattr(self.env, "action_space")
        return None

    def noop_action(self):
        """Return a neutral/no-op action compatible with the environment if possible."""
        if self.tiny:
            return self.env.noop_action()

        if hasattr(self.env, "action_space") and hasattr(self.env.action_space, "empty_action"):
            try:
                return self.env.action_space.empty_action()
            except Exception:
                pass
        # Some environments provide a no_op or noop helper
        if hasattr(self.env, "no_op"):
            try:
                return self.env.no_op()
            except Exception:
                pass
        return None

    def get_obs_dim(self):
        """Return the dimension of the flattened observation vector (if known).

        If not known, perform a reset to compute it.
        """
        if self._obs_dim is not None:
            return self._obs_dim
        # try to compute by resetting
        vec = self.reset()
        return int(vec.shape[0]) if vec is not None else None

    # --- Conversion helpers ---
    def _obs_to_vector(self, obs) -> np.ndarray:
        """Convert various observation representations into a 1D numpy vector.

        Handles dict-like observations, numpy arrays, lists, and tries common
        grid2op observation methods like to_array/to_vect/to_numpy. Falls back to
        extracting numeric attributes if present.
        """
        if obs is None:
            return np.zeros((0,), dtype=np.float32)

        # If it's already a numpy array or list-like
        if isinstance(obs, np.ndarray):
            return obs.ravel().astype(np.float32)
        if isinstance(obs, (list, tuple)):
            return np.asarray(obs, dtype=np.float32).ravel()

        # dict-like
        try:
            if isinstance(obs, dict):
                # flatten numeric values in deterministic order
                vals = []
                for k in sorted(obs.keys()):
                    v = obs[k]
                    if isinstance(v, (int, float)):
                        vals.append(float(v))
                    elif isinstance(v, (list, tuple, np.ndarray)):
                        vals.extend(np.asarray(v).ravel().tolist())
                return np.asarray(vals, dtype=np.float32)
        except Exception:
            pass

        # Try common methods on grid2op.Observation
        for method in ("to_numpy", "to_array", "to_vect", "to_feature_vector", "get_vector"):
            try:
                if hasattr(obs, method):
                    arr = getattr(obs, method)()
                    if isinstance(arr, np.ndarray):
                        return arr.ravel().astype(np.float32)
                    else:
                        return np.asarray(arr, dtype=np.float32).ravel()
            except Exception:
                continue

        # Try to extract attributes commonly present in grid2op observations
        try:
            parts = []
            # production powers
            if hasattr(obs, "prod_p"):
                parts.append(np.asarray(obs.prod_p).ravel())
            if hasattr(obs, "load_p"):
                parts.append(np.asarray(obs.load_p).ravel())
            if hasattr(obs, "rho"):
                parts.append(np.asarray(obs.rho).ravel())
            # voltages
            if hasattr(obs, "prod_v"):
                parts.append(np.asarray(obs.prod_v).ravel())
            if hasattr(obs, "load_v"):
                parts.append(np.asarray(obs.load_v).ravel())
            if parts:
                return np.concatenate([p.astype(np.float32) for p in parts])
        except Exception:
            pass

        # Last resort: try to string-serialize numeric fields
        try:
            s = str(obs)
            nums = [float(tok) for tok in s.replace(',', ' ').split() if _is_number(tok)]
            return np.asarray(nums, dtype=np.float32)
        except Exception:
            pass

        # If nothing works, return empty vector
        return np.zeros((0,), dtype=np.float32)

    def _vector_to_action(self, v: np.ndarray):
        """Best-effort conversion from a numeric vector to a grid2op.Action object.

        Due to API variance across grid2op versions and the complexity of actions,
        this method attempts a few strategies:
        - If the env provides an action_space with a `from_vect` or similar helper,
          use it.
        - If the env provides an `action_space.empty_action()` object, we return it
          (no-op) when we cannot map the vector.

        If mapping is not possible, returns None.
        """
        if v is None:
            return None
        if not hasattr(self, "env") or self.env is None:
            return None

        # Try action_space helpers
        try:
            if hasattr(self.env, "action_space"):
                aspace = getattr(self.env, "action_space")
                for method in ("from_vect", "vector_to_action", "get_action_from_vect"):
                    if hasattr(aspace, method):
                        try:
                            return getattr(aspace, method)(v)
                        except Exception:
                            continue
                # Some versions offer env.action_space.empty_action() or .create()
                if hasattr(aspace, "empty_action"):
                    try:
                        return aspace.empty_action()
                    except Exception:
                        pass
        except Exception:
            pass

        # Try env-specific constructors
        try:
            if hasattr(self.env, "action_space") and hasattr(self.env.action_space, "create"):
                try:
                    return self.env.action_space.create(v)
                except Exception:
                    pass
        except Exception:
            pass

        # Fallback: try to use env.get_action or env.action_space.empty_action()
        try:
            if hasattr(self.env, "get_action"):
                try:
                    return self.env.get_action(v)
                except Exception:
                    pass
        except Exception:
            pass

        # Last resort: return None so caller can use noop_action()
        return None


# --- Tiny fallback environment ---
class _TinyFallbackEnv:
    def __init__(self):
        self.step_count = 0

    def reset(self):
        self.step_count = 0
        return {"t": 0, "loads": [1.0, 1.0], "prods": [1.0, 1.0]}

    def step(self, action):
        self.step_count += 1
        obs = {"t": self.step_count, "loads": [1.0, 1.0], "prods": [1.0, 1.0]}
        reward = 0.0
        done = self.step_count >= 100
        info = {"violations": 0}
        return obs, reward, done, info

    def get_topology(self):
        try:
            import networkx as nx
            G = nx.Graph()
            G.add_nodes_from([0, 1])
            G.add_edge(0, 1)
            return G
        except Exception:
            return None

    def get_observation_space(self):
        return None

    def get_action_space(self):
        return None

    def noop_action(self):
        return None


def _is_number(s: str) -> bool:
    try:
        float(s)
        return True
    except Exception:
        return False
