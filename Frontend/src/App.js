import React, {useState} from 'react';
import './App.css';
import { NavBar } from './Components/NavBar/NavBar';
import { ArticleList } from './Components/ArticleList/ArticleList';

const App  = () => {

  const [category, setCategory] = useState("us")

  return (
      <div>
        <section className="heading">
          <title><h1>WEBSITE TITLE</h1></title>
          {NavBar(setCategory)}
        </section>
        <section className="articleLists">
         {ArticleList(category)}
        </section>
      </div>
    );
}

export default App;
