"""Grid2Op environment adapter (best-effort implementation).

This adapter attempts to use grid2op if available. It provides a thin wrapper that
normalizes the returned values to (observation, reward, done, info) and exposes a
few helper methods used by the demo baseline.

Notes:
- grid2op API surface varies across versions. This adapter uses a defensive style
  and gives informative error messages when grid2op is not installed or the
  requested dataset is missing.
- For quick local tests you can use the --tiny mode which uses a very small
  synthetic environment (implemented in get_fallback_env in this file).
"""
from .base import Environment
from typing import Tuple, Any


class Grid2OpEnv(Environment):
    def __init__(self, env_name: str = "l2rpn_neurips_2020", tiny: bool = False):
        self.env_name = env_name
        self.tiny = tiny
        self.env = None
        if not self.tiny:
            try:
                import grid2op
                # grid2op.create_env or make might be available depending on version
                if hasattr(grid2op, "make"):
                    self.env = grid2op.make(self.env_name)
                elif hasattr(grid2op, "create_env"):
                    self.env = grid2op.create_env(self.env_name)
                else:
                    # legacy: try Environment
                    try:
                        from grid2op.Environment import Environment as G2OEnv
                        self.env = G2OEnv(self.env_name)
                    except Exception:
                        self.env = None
                if self.env is None:
                    raise RuntimeError(
                        "Could not instantiate grid2op environment. Please check your grid2op installation and dataset."
                    )
            except ModuleNotFoundError as e:
                raise ModuleNotFoundError(
                    "grid2op is not installed in your environment. Install grid2op (pip install grid2op) or run in --tiny mode for a local test."
                )
        else:
            # use a lightweight fallback env for local testing
            self.env = self._get_fallback_env()

    def reset(self) -> Any:
        """Reset the underlying env and return an observation object/dict."""
        if self.tiny:
            return self.env.reset()

        # Most grid2op envs expose reset() and a last_obs attribute or return an observation
        try:
            res = self.env.reset()
            # Some versions return observation on reset
            if res is not None:
                return res
            # otherwise try to read last_obs
            if hasattr(self.env, "get_obs"):
                return self.env.get_obs()
            if hasattr(self.env, "observation"):
                return self.env.observation
            if hasattr(self.env, "last_obs"):
                return self.env.last_obs
            return None
        except Exception as e:
            raise RuntimeError(f"Error while resetting grid2op env: {e}")

    def step(self, action) -> Tuple[Any, float, bool, dict]:
        """Apply action. Normalize different return signatures into (obs, reward, done, info)."""
        if self.tiny:
            return self.env.step(action)

        try:
            res = self.env.step(action)
        except TypeError:
            # Some grid2op versions require an action object created via env.action_space
            # Let caller construct a proper action using helper below
            raise
        except Exception as e:
            raise RuntimeError(f"Error during env.step(action): {e}")

        # Normalize:
        # common patterns: (reward, done, info) and observation available via env.get_obs()/last_obs
        if isinstance(res, tuple):
            if len(res) == 3:
                reward, done, info = res
                try:
                    obs = self.env.get_obs() if hasattr(self.env, "get_obs") else getattr(self.env, "last_obs", None)
                except Exception:
                    obs = None
                return obs, reward, done, info
            elif len(res) == 4:
                obs, reward, done, info = res
                return obs, reward, done, info
        # Fallback: try to query latest observation
        obs = None
        try:
            obs = self.env.get_obs() if hasattr(self.env, "get_obs") else getattr(self.env, "last_obs", None)
        except Exception:
            obs = None
        return obs, None, False, {}

    def get_topology(self):
        # Try to return a networkx graph if available
        if self.tiny:
            return self.env.get_topology()

        try:
            if hasattr(self.env, "get_topology"):
                return self.env.get_topology()
            # some envs expose env.simulation or env.grid
            if hasattr(self.env, "grid"):
                return self.env.grid
            return None
        except Exception:
            return None

    def get_observation_space(self):
        if self.tiny:
            return self.env.get_observation_space()
        if hasattr(self.env, "observation_space"):
            return self.env.observation_space
        return None

    def get_action_space(self):
        if self.tiny:
            return self.env.get_action_space()
        if hasattr(self.env, "action_space"):
            return self.env.action_space
        return None

    # Helper used by the baseline model to build a safe "do nothing" action
    def noop_action(self):
        """Return a neutral/no-op action compatible with the environment if possible."""
        if self.tiny:
            return self.env.noop_action()

        # grid2op action creation varies by version. Try common helpers.
        if hasattr(self.env, "action_space") and hasattr(self.env.action_space, "empty_action"):
            try:
                return self.env.action_space.empty_action()
            except Exception:
                pass
        # As a last resort return None; callers should handle it.
        return None


# A tiny fallback environment for local quick tests when grid2op is not installed.
class _TinyFallbackEnv:
    def __init__(self):
        self.step_count = 0

    def reset(self):
        self.step_count = 0
        # return a simple dict observation
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


def _get_fallback_env():
    return _TinyFallbackEnv()

# Expose factory when using tiny mode
Grid2OpEnv._get_fallback_env = staticmethod(_get_fallback_env)
