import React from 'react';
import './App.css';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Search from './components/Search';

function App() {
  return (
    <div className="app-container"> 
      <header className="header"> 
        <Navbar />
      </header>
      <main className="main"> 
        <Search />
      </main>
      <footer className="footer"> 
        <Footer />
      </footer>
    </div>
  );
}

export default App;
