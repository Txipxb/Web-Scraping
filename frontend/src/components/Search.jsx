import React, { useState } from 'react';
import './search.css'; // นำเข้าไฟล์ CSS

function Search() {
  const [searchTerm, setSearchTerm] = useState(""); // เก็บคำค้นหาจากผู้ใช้
  const [results, setResults] = useState([]); // เก็บผลลัพธ์ที่ได้จาก API
  const [loading, setLoading] = useState(false); // กำหนดสถานะการโหลดข้อมูล

  // ฟังก์ชันสำหรับการค้นหา
  const handleSearch = async () => {
    if (!searchTerm) return; // หากไม่มีคำค้นหาไม่ให้ทำการค้นหา
  
    setLoading(true); // ตั้งค่าสถานะเป็นกำลังโหลด
  
    try {
      // เรียก API ที่ Flask server
      const response = await fetch(`http://localhost:5000/search_JIB?q=${searchTerm}`);

  
      // ตรวจสอบสถานะการตอบกลับจากเซิร์ฟเวอร์
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      // แปลงผลลัพธ์เป็น JSON
      const data = await response.json();
  
      // อัพเดตผลลัพธ์การค้นหา
      setResults(data);
    } catch (error) {
      // แสดงข้อผิดพลาดที่เกิดขึ้น
      alert(`Error fetching data: ${error.message}`);
    } finally {
      setLoading(false); // สถานะโหลดเสร็จสิ้น
    }
  };

  return (
    <div className="search-container">
        <div className='search-title'>Search Products</div>
      <input
        type="text"
        className="search-input"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        placeholder="Search products..."
      />
      <button
        onClick={handleSearch}
        className="search-button"
        disabled={loading}
      >
        {loading ? 'Searching...' : 'Search'}
      </button>

      {results.length > 0 ? (
  <ul className="results-list">
    {results.map((item, index) => (
      <li key={index} className="result-card">
        <img className="product-image" src={item.image_url} alt={item.name} />
        <div className="product-details">
          <p className="product-name">{item.name}</p>
          <p className="product-price">{item.price}</p>
          <a 
            href={item.product_url} 
            target="_blank" 
            rel="noopener noreferrer" 
            className="view-button"
          >
            View Product
          </a>
        </div>
      </li>
    ))}
  </ul>
) : (
  <p className="no-results">
    {loading ? 'Searching...' : 'No results found'}
  </p>
)}
    </div>
  );
}

export default Search;
