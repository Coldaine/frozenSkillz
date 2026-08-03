## Required when using the browser

When acting as the primary or coordinating agent, always delegate browser tasks to the `chrome_pilot` custom subagent when browser use is required. This rule does not apply inside the `chrome_pilot` worker itself.

Give `chrome_pilot` the requested outcome, relevant starting tab or URL, authorization boundaries, and stop condition. Then use its result to continue the task.
