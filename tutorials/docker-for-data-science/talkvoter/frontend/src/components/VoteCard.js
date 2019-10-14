import React, { Component } from 'react';
import {
  Card, CardHeader, CardBody, CardTitle, CardSubtitle, CardText,
  Button } from 'reactstrap';

class VoteCard extends Component {
  constructor(props) {
    super(props);
    this.state = {
        result: {},
        talk_id: null,
    };
    this.fetchRandomTalk();
  }

  fetchRandomTalk() {
    /*
    Hit Flask endpoint to get talk from last year that user has not voted on
    */
    fetch('/api/v1/talks/random/', {
      method: 'GET',
      headers: {'Content-Type': 'application/json'},
      credentials: "same-origin",
    })
    .then(response => response.json())
    .then(data => this.setState({
      result: data,
      talk_id: data['id'],
    }));
  }

  vote(event, vote_type) {
    /*
    Process vote user vote and load next talk
    */
    event.preventDefault();

    let body_ = {
      "vote": null
    };

    if (vote_type === 'yes') {
      body_['vote'] = 'in_person'
    } else {
      body_['vote'] = 'watch_later'
    }

    let that = this;  // this trick never fails :D

    fetch('/api/v1/talks/' + this.state.talk_id + '/vote/', {
        method: 'POST',
        body: JSON.stringify(body_),
        headers: {'Content-Type': 'application/json'},
        credentials: "same-origin",
    })
    .then(function(response) {
      if (response.status === 200) {
        that.fetchRandomTalk();
      } else if (response.status === 404) {
        // TODO: voted on all talks, go to predict
        console.log('Voted on all talks, time to predict')
      }
    });
  }

  render() {
    return (
      <Card>
        <CardHeader>
          <Button color="danger" className="float-left" onClick={(e) => this.vote(e, 'no')}>
            Watch Later
          </Button>
          <Button color="success" className="float-right" onClick={(e) => this.vote(e, 'yes')}>
            In Person
          </Button>
        </CardHeader>
        <CardBody>
          <CardTitle tag="h3" className="text-center">{this.state.result['title']}</CardTitle>
          <CardSubtitle className="text-center">
            <small>Presented by: {this.state.result['presenters']}</small>
          </CardSubtitle>
          <br />
          <CardText>{this.state.result['description']}</CardText>
        </CardBody>
      </Card>
    );
  }
}

export default VoteCard;
