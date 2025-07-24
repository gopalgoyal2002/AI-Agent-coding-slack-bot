// slack-mcp.js
const express = require("express");
const axios = require("axios");

const app = express();
app.use(express.json());

const SLACK_TOKEN = process.env.SLACK_TOKEN; // Set in terminal or .env
const SLACK_CHANNEL = process.env.SLACK_CHANNEL; // Set in terminal or .env

app.post("/slack/send", async (req, res) => {
  const { query } = req.body;

  try {
    const response = await axios.post(
      "https://slack.com/api/chat.postMessage",
      {
        channel: SLACK_CHANNEL,
        text: query,
      },
      {
        headers: {
          Authorization: `Bearer ${SLACK_TOKEN}`,
          "Content-Type": "application/json",
        },
      }
    );

    if (response.data.ok) {
      res.status(200).send({ status: "sent" });
    } else {
      res.status(500).send({ error: response.data.error });
    }
  } catch (err) {
    res.status(500).send({ error: err.message });
  }
});

app.listen(8000, () => {
  console.log("Slack MCP server running at http://localhost:8000/slack/send");
});
