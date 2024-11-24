import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const PaperDetail = () => {
  const { filename } = useParams();
  const [paper, setPaper] = useState(null);

  useEffect(() => {
    axios.get(`http://localhost:8000/api/papers/${filename}/`)
      .then((res) => {
        setPaper(res.data);
      })
      .catch((err) => {
        console.error(err);
      });
  }, [filename]);

  if (!paper) return <div>Loading...</div>;

  return (
    <div>
      <h1>{paper.title}</h1>
      <h3>Summary</h3>
      <p>{paper.summary}</p>
      <h3>Table Data</h3>
      <pre>{JSON.stringify(paper.table_data, null, 2)}</pre>
    </div>
  );
};

export default PaperDetail;