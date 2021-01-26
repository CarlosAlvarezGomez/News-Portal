import { useEffect, useState } from 'react';
import axios from 'axios';

export function useGetArticles(category, pageNumber) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [articles, setArticles] = useState([]);
  const [hasMore, setHasMore] = useState(false);

  useEffect(() =>  {
    setLoading(true);
    setError(false);

    // Requst next page of articles from api and append it to current list of
    // articles
    var newArticles = []
    for (var i=0; i < 10; i++) {
      axios({
        method: 'GET',
        url:'http://localhost:8081/articles/',
        params: {category: category, requestNumber: 0}
      }).then(res => {
        newArticles.concat(res.data)
      })
      
    }
    setArticles(articles.concat(newArticles))

    setHasMore(true);
    setLoading(false);
  }, [pageNumber])

  useEffect(() => {
    setLoading(true);
    setError(false);

    // Requst first page of articles for new category from api and append it to
    // current list of articles
    var newArticles = []
    axios({
      method: 'GET',
      url:'url',
      params: {category: category, requestNumber: 0}
    }).then(res => {
      newArticles = res.data
      setArticles(newArticles)
    })

    setHasMore(true);
    setLoading(false);
  }, [category])
  return { loading, error, articles, hasMore };
}