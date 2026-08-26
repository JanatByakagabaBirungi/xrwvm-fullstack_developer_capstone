const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');
const app = express();
const port = 3030;

app.use(cors());
app.use(express.urlencoded({ extended: false }));

// Load models
SessionsData = require('./dealership');
ReviewsData = require('./review');

// Connect to MongoDB
mongoose.connect('mongodb://mongo_db:27017/dealershipsDB');

// 1. Fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await ReviewsData.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching reviews' });
  }
});

// 2. Fetch reviews by dealer ID (Task 8)
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await ReviewsData.find({ dealership: req.params.id });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching reviews for dealer' });
  }
});

// 3. Fetch all dealerships (Task 9)
app.get('/fetchDealers', async (req, res) => {
  try {
    const dealerships = await SessionsData.find();
    res.json(dealerships);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships' });
  }
});

// 4. Fetch dealerships by state (Task 11)
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const dealerships = await SessionsData.find({ state: req.params.state });
    res.json(dealerships);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships by state' });
  }
});

// 5. Fetch dealer by ID (Task 10)
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const dealership = await SessionsData.findOne({ id: req.params.id });
    res.json(dealership);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealership by ID' });
  }
});

// 6. Insert review
app.post('/insert_review', express.json(), async (req, res) => {
  try {
    const data = req.body;
    const documents = await ReviewsData.create(data);
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error inserting review' });
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});