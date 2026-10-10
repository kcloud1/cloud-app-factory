// Static assets only. No API, credentials, or cloud resource creation.
export default {
  async fetch(request, env) {
    return env.ASSETS.fetch(request);
  }
};
