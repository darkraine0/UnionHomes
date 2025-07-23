import React, { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import { Chart, LineElement, PointElement, LinearScale, Title, CategoryScale, Tooltip, Legend } from "chart.js";
import { Link } from "react-router-dom";

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
  "DR Horton": "#e11d48", // rose-600
  "UnionMain Homes": "#2563eb", // blue-600
};
const COMPANY_BG_COLORS: Record<string, string> = {
  "DR Horton": "#f43f5e", // rose-500
  "UnionMain Homes": "#60a5fa", // blue-400
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
      borderColor: COMPANY_COLORS[company] || '#888',
      backgroundColor: COMPANY_BG_COLORS[company] || '#bbb',
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
        labels: { font: { weight: "bold" } },
      },
      title: {
        display: true,
        text: `Price vs Sqft by Company`,
        color: "#e11d48",
        font: { size: 22, weight: "bold" },
      },
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
        title: { display: true, text: "Sqft", color: "#e11d48", font: { weight: "bold" } },
        ticks: { color: "#e11d48" },
        grid: { color: "#fda4af" },
        type: 'linear',
      },
      y: {
        title: { display: true, text: "Price ($)", color: "#e11d48", font: { weight: "bold" } },
        ticks: { color: "#e11d48" },
        grid: { color: "#fda4af" },
      },
    },
  } as any;

  return (
    <div className="min-h-screen bg-gradient-to-br from-rose-50 via-rose-100 to-rose-200 p-4 flex flex-col items-center">
      <div className="w-full max-w-4xl bg-white rounded-lg shadow p-6 mt-8">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-3xl font-bold text-rose-700">Price vs Sqft Line Chart by Company</h2>
          <Link to="/">
            <button className="px-4 py-2 rounded bg-gradient-to-r from-rose-700 to-rose-500 text-white hover:from-rose-800 hover:to-rose-600 font-bold shadow">
              ← Back to Table
            </button>
          </Link>
        </div>
        {loading ? (
          <div className="text-center text-rose-400">Loading...</div>
        ) : error ? (
          <div className="text-center text-rose-600 font-semibold">{error}</div>
        ) : (
          <Line data={data} options={options} />
        )}
      </div>
    </div>
  );
};

export default ChartPage; 