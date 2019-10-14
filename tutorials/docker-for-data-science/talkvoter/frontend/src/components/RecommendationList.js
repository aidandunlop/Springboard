import React, { Component } from 'react';
import {
  Card, CardBody, CardFooter, CardTitle, CardSubtitle, CardText,
  Button } from 'reactstrap';

class RecommendationList extends Component {
  constructor(props) {
    super(props);
    this.state = {talks: []}
    this.getTalkRecommendations();
  }

  getTalkRecommendations() {
    /*
    Hit Flask endpoint to get talk recommendations for current year
    */
    fetch('/api/v1/predict/', {
      method: 'GET',
      headers: {'Content-Type': 'application/json'},
      credentials: "same-origin",
    })
    .then(response => response.json())
    .then(response => this.setState({talks : response['predicted_talks']}));
  }

  render() {
    let talks = this.state.talks;
    if (talks.length == 0)
        return <h3>Not enough talks were selected. Please label some <a href="/">more</a>.</h3>
    return (
      talks.map( talk =>
      <Card>
        <CardBody>
          <CardTitle tag="h3" className="text-center">{talk['title']}</CardTitle>
          <CardSubtitle className="text-center">
            <small>Presented by: {talk['presenters']}</small><br />
            <small>Location: {talk['location']}</small>
          </CardSubtitle>
          <br />
          <CardText>{talk['description']}</CardText>
        </CardBody>
      </Card>
      )
    );
  }
}

export default RecommendationList;
