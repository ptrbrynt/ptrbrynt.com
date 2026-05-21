export async function onRequest(context) {
  const { searchParams } = new URL(context.request.url);
  const redirectUrl = new URL("https://github.com/login/oauth/authorize");
  redirectUrl.searchParams.set("client_id", context.env.GITHUB_CLIENT_ID);
  redirectUrl.searchParams.set("scope", "repo");
  const state = searchParams.get("state") || "";
  redirectUrl.searchParams.set("state", state);
  return Response.redirect(redirectUrl.toString(), 302);
}
