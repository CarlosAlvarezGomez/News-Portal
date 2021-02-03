import React from 'react';
import './Main.css';
import { NavBar } from './Components/NavBar/NavBar';
import { ArticleList } from './Components/ArticleList/ArticleList';

const Main  = () => {
  
  const tabs = ["us", "world", "politics", "business", "health", "entertainment", "opinion"];
  
  const urlParams = window.location.toString().substring(22).split('/')
  var cat = ''
  if (tabs.indexOf(urlParams[0].toLowerCase()) !== -1) {
    cat = urlParams[0]
  } else {
    cat = 'us'
  }
  const category = cat


  return (
      <div>
        <section className="heading">
          <title><h1>NEWS-PORTAL</h1></title>
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
