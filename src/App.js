import React from 'react';
import './App.css';
import { NavBar } from './Components/NavBar/NavBar';
import { ArticleList } from './Components/ArticleList/ArticleList';
import { render } from '@testing-library/react';


class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { category: "us" };
    this.handleNavBarClick = this.handleNavBarClick.bind(this)
  }

  handleNavBarClick(cat) {
    this.setState({ category: cat })
  }

  render() {
    return (
      <div>
        <section className="heading">
          <h1 className="heading">WEBSITE NAME</h1>
          <NavBar onButtonClick={this.handleNavBarClick} className="heading" />
        </section>
        <section className="articleLists">
          <ArticleList className="artricleList" category={this.state.category} />
        </section>
      </div>
    );
  }
}

export default App;
