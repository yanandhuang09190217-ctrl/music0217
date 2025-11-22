Deploy instructions:
1. Upload this project to a GitHub repository.
2. On Render create a new "Web Service" and link to the repo.
   - Environment variable required: DISCORD_TOKEN = <your bot token>
3. Use Docker as the environment (Render will use the Dockerfile).
4. Deploy. Logs should show Lavalink starting and bot logging in.

Notes:
- Render free instances sleep after inactivity; for persistent music usage consider a VPS or paid plan.
