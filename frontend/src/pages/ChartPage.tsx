import React, { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import { Chart, LineElement, PointElement, LinearScale, Title, CategoryScale, Tooltip, Legend } from "chart.js";
import { Link } from "react-router-dom";
import Loader from "../components/Loader";
import ErrorMessage from "../components/ErrorMessage";

Chart.register(LineElement, PointElement, LinearScale, Title, CategoryScale, Tooltip, Legend);

interface Plan {
  plan_name: string;
  price: number;
  sqft: number;
  stories: string;
  price_per_sqft: number;
  last_updated: string;
  price_changed_recently: boolean;
  company: string;
  community: string;
}

const API_URL = "http://localhost:8080/api/plans";

const COMPANY_COLORS: Record<string, string> = {
  "DR Horton": "#7288ff",
  "UnionMain Homes": "#00cfff",
};
const COMPANY_BG_COLORS: Record<string, string> = {
  "DR Horton": "#7288ff",
  "UnionMain Homes": "#00cfff",
};

const ChartPage: React.FC<{ selectedCompany: string }> = ({ selectedCompany }) => {
  const [plans, setPlans] = useState<Plan[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchPlans = async () => {
      setLoading(true);
      setError("");
      try {
        const res = await fetch(API_URL);
        if (!res.ok) throw new Error("Failed to fetch plans");
        const data = await res.json();
        setPlans(data);
      } catch (err: any) {
        setError(err.message || "Unknown error");
      } finally {
        setLoading(false);
      }
    };
    fetchPlans();
  }, []);

  // Get all companies present
  const companies = Array.from(new Set(plans.map((p) => p.company)));

  // Prepare datasets for each company
  const datasets = companies.map((company) => {
    const filtered = plans.filter((p) => p.company === company && p.sqft && p.price);
    // Sort by sqft for a smooth line
    const sorted = filtered.sort((a, b) => a.sqft - b.sqft);
    return {
      label: company,
      data: sorted.map((p) => ({ x: p.sqft, y: p.price })),
      borderColor: COMPANY_COLORS[company] || '#7288ff',
      backgroundColor: COMPANY_BG_COLORS[company] || '#00cfff',
      tension: 0.2,
      pointRadius: 4,
      pointHoverRadius: 6,
      fill: false,
    };
  });

  // X axis: all unique sqft values (sorted)
  const allSqft = Array.from(new Set(plans.filter((p) => p.sqft).map((p) => p.sqft))).sort((a, b) => a - b);

  const data = {
    labels: allSqft,
    datasets,
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        display: true,
        labels: { font: { weight: "bold" }, color: '#7288ff' },
      },
      // title: {
      //   display: true,
      //   text: `Price vs Sqft by Company`,
      //   color: "#7288ff",
      //   font: { size: 22, weight: "bold" },
      // },
      tooltip: {
        callbacks: {
          label: function (context: any) {
            const d = context.raw;
            return `Sqft: ${d.x} | Price: $${d.y.toLocaleString()}`;
          },
        },
      },
    },
    scales: {
      x: {
        title: { display: true, text: "Sqft", color: "#7288ff", font: { weight: "bold" } },
        ticks: { color: "#7288ff" },
        grid: { color: "#e0e7ff" },
        type: 'linear',
      },
      y: {
        title: { display: true, text: "Price ($)", color: "#7288ff", font: { weight: "bold" } },
        ticks: { color: "#7288ff" },
        grid: { color: "#e0e7ff" },
      },
    },
  } as any;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-cyan-50 to-blue-100 p-4 flex flex-col items-center">
      <div className="w-full max-w-6xl bg-white rounded-lg shadow p-6 mt-8">
        <div className="flex justify-between items-center mb-8">
          <h2 style={{ color: '#7288ff' }} className="text-3xl font-bold">Price vs Sqft Line Chart by Company</h2>
          <Link to="/">
            <button className="px-4 py-2 rounded" style={{ background: 'linear-gradient(to right, #7288ff, #00cfff)', color: '#fff', fontWeight: 'bold', boxShadow: '0 2px 8px #7288ff33' }}>
              ← Back to Table
            </button>
          </Link>
        </div>
        {loading ? (
          <Loader />
        ) : error ? (
          <ErrorMessage message={error} />
        ) : (
          <Line data={data} options={options} />
        )}
      </div>
    </div>
  );
};

export default ChartPage; 