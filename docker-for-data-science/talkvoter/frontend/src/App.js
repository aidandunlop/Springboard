import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Link, Switch } from 'react-router-dom';
import {
  Container, Row, Col,
  Navbar, NavbarBrand, Nav,
  UncontrolledDropdown, DropdownToggle, DropdownMenu, DropdownItem } from 'reactstrap';

import VoteCard from './components/VoteCard';
import RecommendationList from './components/RecommendationList';

import './App.css';


const NavigationBar = () => (
  <Navbar color="dark" dark expand="md">
    <NavbarBrand className="mx-auto" href="/">
      <div className="navbar-title">Talk Recommender</div>
    </NavbarBrand>

    <Nav navbar>
      <UncontrolledDropdown nav inNavbar>
        <DropdownToggle nav caret></DropdownToggle>
        <DropdownMenu right>
          <DropdownItem tag={Link} to="/">Vote</DropdownItem>
          <DropdownItem tag={Link} to="/recommendations">Recommendations</DropdownItem>
          <DropdownItem divider />
          <DropdownItem href="/login">Login</DropdownItem>
          <DropdownItem href="/logout">Logout</DropdownItem>
        </DropdownMenu>
      </UncontrolledDropdown>
    </Nav>
  </Navbar>
)

const Content = () => (
  <Container>
    <Row>
      <Col>
        <Switch>
          <Route exact path="/" component={VoteCard} />
          <Route path="/recommendations" component={RecommendationList} />
        </Switch>
      </Col>
    </Row>
  </Container>
)

const Layout = () => (
  <Router>
    <div>
      <NavigationBar />
      <br />
      <Content />
    </div>
  </Router>
)

class App extends Component {
  render() {
    return (
      <Layout />
    );
  }
}

export default App;
