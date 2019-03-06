<h1>Setting Up Slack Notifications with Foundations</h1>

**NOTE:** This feature is **EXPERIMENTAL** and may be subject to change in future releases.

Foundations integrates directly with slack, and can signal jobs events (Queued, Running, Completed) to user-specified channels.

##Setup##
To setup Slack notifications, you will need to provide the slack API token as an environment variable before setting up Foundations. The Foundations integrations team will help assist in setting this up.

```bash
export FOUNDATIONS_SLACK_TOKEN=<API_TOKEN>
```

##Deploying Jobs##
Once Foundations has been setup with the `FOUNDATIONS_SLACK_TOKEN`, you can specify the slack channel where you want the notifications to be pushed to with via the `foundations.config_mananger`. For example, adding the following line to your driver code will push job event notifications to the `spamity` channel:

```
foundations.config_manager['job_notification_channel'] = 'spamity'
```