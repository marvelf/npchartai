const express = require('express');
const app = express();
const port = process.env.PORT || 3000; // This will use the port set in an environment variable or 5000 if not set.


app.get('/', (req, res) => {
  res.send('Web App!');
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});