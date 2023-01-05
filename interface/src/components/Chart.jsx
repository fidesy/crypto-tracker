import "chartjs-adapter-date-fns";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    TimeScale,
    Tooltip,
    Legend,
  } from 'chart.js';
import { Line } from "react-chartjs-2"

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    TimeScale,
    Tooltip,
    Legend
  );

ChartJS.defaults.font.family = "Montserrat, sans-serif"

export default function Chart({ candlesticks, title }) {
    const options = {
        responsive: true,
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'month'
                },
                // remove grids from the chart
                grid: {
                    drawOnChartArea: false,
                }
            }, 
            y: {
                // remove grids from the chart
                grid: {
                    drawOnChartArea: false,
                }
            }        
        },
        plugins: {
          legend: {
            // position: 'top',
            display: false,
          },
          title: {
            display: true,
            text: title,
          },
        }
    }

    return (
        <Line options={options} data={{
            labels: candlesticks.map(candle => candle["date"]),
            datasets: [
                {
                    // label: "Price",
                    data: candlesticks.map(candle => candle["close"]),
                    pointRadius: 0,
                    borderColor: "rgb(75, 192, 192)",
                    tension: 0.5,
                }
            ]
        }}/>
    )
}