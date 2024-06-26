import React, { useState } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';

const PlotlyGraph = () => {
    const [graphData, setGraphData] = useState(null);
    const [formData, setFormData] = useState({
        symbol: '',
        from_date: '',
        to_date: '',
    });

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const { symbol, from_date, to_date } = formData;
        axios
            .post('/api/fetch-data', { symbol, from_date, to_date })
            .then((response) => {
                setGraphData(response.data);
            })
            .catch((error) => console.error(error));
    };

    return (
        <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
            <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
                <label>
                    Symbol:
                    <input
                        type="text"
                        name="symbol"
                        value={formData.symbol}
                        onChange={handleChange}
                        style={{ margin: '0 10px' }}
                    />
                </label>
                <label>
                    From Date:
                    <input
                        type="text"
                        name="from_date"
                        value={formData.from_date}
                        onChange={handleChange}
                        style={{ margin: '0 10px' }}
                    />
                </label>
                <label>
                    To Date:
                    <input
                        type="text"
                        name="to_date"
                        value={formData.to_date}
                        onChange={handleChange}
                        style={{ margin: '0 10px' }}
                    />
                </label>
                <button type="submit">Fetch Data</button>
            </form>
            {graphData && (
                <Plot
                    data={[
                        {
                            x: graphData.x,
                            y: graphData.y,
                            type: 'bar',
                            mode: 'lines+markers',
                            name: 'Deliverable Quantity',
                            marker: { color: 'blue', size: 8 },
                            line: {  smoothing: 1.3, color: 'blue' },
                            
                            
                        },
                    ]}
                    layout={{
                        title: {
                            text: 'Line Plot of Deliverable Quantity Over Time',
                            font: {
                                family: 'Arial, sans-serif',
                                size: 24,
                                color: 'red',
                            },
                        },
                        xaxis: {
                            title: {
                                text: 'Date',
                                font: {
                                    family: 'Arial, sans-serif',
                                    size: 18,
                                    color: 'red',
                                },
                            },
                            tickformat: '%d-%b-%Y',
                            showgrid: true,
                            zeroline: true,
                            gridcolor: '#e9e9e9',
                        },
                        yaxis: {
                            title: {
                                text: 'Deliverable Quantity',
                                font: {
                                    family: 'Arial, sans-serif',
                                    size: 18,
                                    color: '#333',
                                },
                            },
                            showgrid: true,
                            zeroline: true,
                            gridcolor: '#e9e9e9',
                        },
                        template: 'plotly',
                        width: 800,
                        height:500,
                        margin: { t: 50, b: 50, l: 50, r: 50 },
                        paper_bgcolor: 'white',
                        plot_bgcolor: '#e5ecf6',
                        hovermode: 'closest',
                      
                        
                    }}
                    config={{
                        responsive: true,
                        displayModeBar: true,
                      
                       modeBarButtonsToRemove: [  'lasso2d',
                            'select2d',
                            'sendDataToCloud',
                            'zoomIn2d',
                            'zoomOut2d',
                            'autoScale2d',
                            'resetScale2d',
                            'toggleSpikelines',
                            'hoverClosestCartesian',
                            'hoverCompareCartesian',
                            'zoom2d','orbitRotation','v1hovermode']
                    }}
                />
            )}
        </div>
    );
};

const App = () => (
    <div>
        <h1 style={{ textAlign: 'center', fontFamily: 'Arial, sans-serif' }}>Interactive Plotly Graph</h1>
        <PlotlyGraph />
    </div>
);

export default App;
