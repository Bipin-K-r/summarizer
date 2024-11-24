import React, { useEffect, useState } from 'react';
import axios from 'axios';

const PaperList = () => {
  const [papers, setPapers] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/api/papers/')
      .then((res) => {
        setPapers(res.data);
      })
      .catch((err) => {
        console.error(err);
      });
  }, []);

  return (
    <div>
      <h1>Available Papers</h1>
      <div className="paper-list">
        {papers.map((paper) => (
          <div key={paper.filename} className="paper-card" onClick={() => window.location.href = `/paper/${paper.filename}`}>
            <h3>{paper.title}</h3>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PaperList;