import React from 'react';
import './Main.css';
import { NavBar } from './Components/NavBar/NavBar';
import { ArticleList } from './Components/ArticleList/ArticleList';

const Main  = () => {
  
  const tabs = ["us", "world", "politics", "business", "health", "entertainment", "opinion"];
  
  // Tries to find a category in link
  const urlParams = window.location.toString().substring(22).split('/')
  var category = ''
  if (tabs.indexOf(urlParams[0].toLowerCase()) !== -1) {
    category = urlParams[0]
  
  // Sets category to 'us' if no category is found
  } else {
    category = 'us'
  }

  return (
      <div>
        <section className="heading">
          <title><h1>NEWS PALATE</h1></title>
          <div className="navBar">
            {NavBar()}
          </div>
        </section>
        <section className="articleLists">
         {ArticleList(category)}
        </section>
      </div>
    );
}

export default Main;
