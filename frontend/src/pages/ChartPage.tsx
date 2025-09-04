import React, { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import { Chart, LineElement, PointElement, LinearScale, Title, CategoryScale, Tooltip, Legend } from "chart.js";
import { useParams, useNavigate, useSearchParams } from "react-router-dom";
import TypeTabs from "../components/TypeTabs";
import Loader from "../components/Loader";
import ErrorMessage from "../components/ErrorMessage";
import API_URL from '../config';
import { getCompanyColor } from '../utils/colors';


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
  type: string;
}



const ChartPage: React.FC = () => {
  const { communityName } = useParams<{ communityName: string }>();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [plans, setPlans] = useState<Plan[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  
  // Get the type from URL parameter, default to 'now' if not specified
  const urlType = searchParams.get('type');
  const [selectedType, setSelectedType] = useState<string>(urlType === 'plan' ? 'Plan' : 'Now');

  const decodedCommunityName = communityName ? decodeURIComponent(communityName) : '';

  useEffect(() => {
    const fetchPlans = async () => {
      setLoading(true);
      setError("");
      try {
        const res = await fetch(API_URL + "/plans");
        if (!res.ok) throw new Error("Failed to fetch plans");
        const data = await res.json();
        
        // Filter plans for this specific community
        const communityPlans = data.filter((plan: Plan) => plan.community === decodedCommunityName);
        setPlans(communityPlans);
      } catch (err: any) {
        setError(err.message || "Unknown error");
      } finally {
        setLoading(false);
      }
    };
    
    if (decodedCommunityName) {
      fetchPlans();
    }
  }, [decodedCommunityName]);

  if (!decodedCommunityName) {
    return <ErrorMessage message="Community not found" />;
  }

  // Filter plans by selected type
  const filteredPlans = plans.filter((plan) => 
    selectedType === 'Plan' || selectedType === 'Now' ? plan.type === selectedType.toLowerCase() : true
  );

  // Get all companies present in filtered data
  const companies = Array.from(new Set(filteredPlans.map((p) => p.company)));

  // Prepare datasets for each company
  const datasets = companies.map((company) => {
    const filtered = filteredPlans.filter((p) => p.company === company && p.sqft && p.price);
    // Sort by sqft for a smooth line
    const sorted = filtered.sort((a, b) => a.sqft - b.sqft);
    return {
      label: company,
      data: sorted.map((p) => ({ x: p.sqft, y: p.price })),
      borderColor: getCompanyColor(company),
      backgroundColor: getCompanyColor(company) + '40', // Add 40 for transparency
      tension: 0.2,
      pointRadius: 4,
      pointHoverRadius: 6,
      fill: false,
    };
  });

  // X axis: all unique sqft values (sorted) from filtered data
  const allSqft = Array.from(new Set(filteredPlans.filter((p) => p.sqft).map((p) => p.sqft))).sort((a, b) => a - b);

  const data = {
    labels: allSqft,
    datasets,
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        display: true,
        labels: { font: { weight: "bold" }, color: '#2563eb' },
      },
      title: {
        display: true,
        text: `${decodedCommunityName} - Price vs Sqft by Company - ${selectedType} Homes`,
        color: "#2563eb",
        font: { size: 18, weight: "bold" },
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
        title: { display: true, text: "Sqft", color: "#2563eb", font: { weight: "bold" } },
        ticks: { color: "#2563eb" },
        grid: { color: "#dbeafe" },
        type: 'linear',
      },
      y: {
        title: { display: true, text: "Price ($)", color: "#2563eb", font: { weight: "bold" } },
        ticks: { color: "#2563eb" },
        grid: { color: "#dbeafe" },
      },
    },
  } as any;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-cyan-50 to-blue-100 p-4 flex flex-col items-center">
      <div className="w-full max-w-6xl bg-white rounded-lg shadow p-6 mt-8">
        <div className="flex justify-between items-center mb-8">
          <h2 style={{ color: '#2563eb' }} className="text-3xl font-bold">{decodedCommunityName} - Price Analysis</h2>
          <div className="flex gap-4">
            <button 
              onClick={() => navigate(`/community/${encodeURIComponent(decodedCommunityName)}`)}
              className="px-4 py-2 rounded bg-gray-600 text-white font-semibold hover:bg-gray-700 transition"
            >
              ← Back to Community
            </button>
          </div>
        </div>
        
        <TypeTabs selected={selectedType} onSelect={setSelectedType} />
        
        {loading ? (
          <Loader />
        ) : error ? (
          <ErrorMessage message={error} />
        ) : (
          <div>
            {filteredPlans.length === 0 ? (
              <div className="text-center py-12">
                <p className="text-lg text-gray-500">No {selectedType.toLowerCase()} homes found in {decodedCommunityName} to display in the chart.</p>
              </div>
            ) : (
              <Line data={data} options={options} />
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ChartPage; 