import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Search, Filter } from 'lucide-react';
import "../styles/HomePage.module.css";

const HomePage = ({ onSearch, onFilter }) => {
    const [searchTerm, setSearchTerm] = useState('');
    const [filter, setFilter] = useState('All');

    const handleSearchChange = (e) => setSearchTerm(e.target.value);
    const handleFilterChange = (e) => {
        setFilter(e.target.value);
        onFilter(e.target.value);
    };
    const handleSearchClick = () => onSearch(searchTerm);

    return (
        <>
            <nav className="navbar navbar-expand-lg  fixed-top bg-dark">
                <div className="container-fluid">
                    <a className="navbar-brand" href="#" style={{color:'red'}}>InfluenceIQ</a>
                    <button
                        className="navbar-toggler"
                        type="button"
                        data-bs-toggle="collapse"
                        data-bs-target="#navbarSupportedContent"
                        aria-controls="navbarSupportedContent"
                        aria-expanded="false"
                        aria-label="Toggle navigation"
                    >
                        <span className="navbar-toggler-icon"></span>
                    </button>

                    <div className="collapse navbar-collapse" id="navbarSupportedContent">
                        {/* Search Bar Section */}
                        <form className="d-flex me-2 flex-grow-1" role="search">
                            <div className="input-group w-75 search-bar">
                                <span className="input-group-text">
                                    <Search size={16} />
                                </span>
                                <input
                                    className="form-control"
                                    type="search"
                                    placeholder="Search..."
                                    value={searchTerm}
                                    onChange={handleSearchChange}
                                />
                                <button className="btn btn-outline-success " type="button" onClick={handleSearchClick} style={{ color: 'white' , border:"2px solid purple" }}>Find</button>
                            </div>
                        </form>

                        {/* Filter Section */}
                        <div className="input-group w-25" style={{ maxWidth: '180px',cursor:'pointer' }}>
                            <span className="input-group-text">
                                <Filter size={16} />
                            </span>
                            <select className="form-select" value={filter} onChange={handleFilterChange} style={{cursor:'pointer'}}>
                                <option value="All">All</option>
                                <option value="Education">Education</option>
                                <option value="Fitness">Fitness</option>
                                <option value="Technology">Technology</option>
                                <option value="Health">Health</option>
                            </select>
                        </div>
                    </div>
                </div>
            </nav>

        </>
    );
};

export default HomePage;
