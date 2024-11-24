import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import PaperList from './components/PaperList.jsx';
import PaperDetail from './components/PaperDetail.jsx';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<PaperList />} />
          <Route path="/paper/:filename" element={<PaperDetail />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
