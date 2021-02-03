import { useEffect, useState } from 'react';
import axios from 'axios';

export function useGetArticles(category, pageNumber, setPageNumber) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [articles, setArticles] = useState([]);
  const [hasMore, setHasMore] = useState(false);

  useEffect(() =>  {
    setLoading(true);
    setError(false);

    // Requst next page of articles from api and append it to current list of
    // articles
    for (var i=0; i < 10; i++) {
      axios({
        method: 'GET',
        url:'http://localhost:8081/articles/',
        params: {category: category, requestNumber: pageNumber}
      }).then(res => {
        setArticles([... articles, ...res.data])
      }).catch( err => {
        setError(true)
      })
      
    }

    // setArticles(articles.concat(newArticles))

    setHasMore(true);
    setLoading(false);
  }, [pageNumber])

  return { loading, error, articles, hasMore };
}