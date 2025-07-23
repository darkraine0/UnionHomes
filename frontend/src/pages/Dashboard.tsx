import React, { useEffect, useState } from "react";
import CompanyTabs from "../components/CompanyTabs";
import Loader from "../components/Loader";
import ErrorMessage from "../components/ErrorMessage";

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

type SortKey = "plan_name" | "price" | "sqft" | "last_updated";
type SortOrder = "asc" | "desc";
const PAGE_SIZE = 50;

const Dashboard: React.FC = () => {
  const [plans, setPlans] = useState<Plan[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [filter, setFilter] = useState("");
  const [sortKey, setSortKey] = useState<SortKey>("price");
  const [sortOrder, setSortOrder] = useState<SortOrder>("asc");
  const [page, setPage] = useState(1);
  const [selectedCompany, setSelectedCompany] = useState<string>('All');

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

  useEffect(() => {
    fetchPlans();
    const interval = setInterval(fetchPlans, 60 * 1000); // Refresh every 1 min
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    setPage(1); // Reset to first page on filter/sort change
  }, [filter, sortKey, sortOrder, selectedCompany]);

  const companies = Array.from(new Set(plans.map((p) => p.company)));

  const filteredPlans = plans.filter((plan) =>
    (selectedCompany === 'All' || plan.company === selectedCompany) &&
    plan.plan_name.toLowerCase().includes(filter.toLowerCase())
  );

  const sortedPlans = [...filteredPlans].sort((a, b) => {
    let aValue: any = a[sortKey];
    let bValue: any = b[sortKey];
    if (sortKey === "last_updated") {
      aValue = new Date(aValue).getTime();
      bValue = new Date(bValue).getTime();
    }
    if (aValue < bValue) return sortOrder === "asc" ? -1 : 1;
    if (aValue > bValue) return sortOrder === "asc" ? 1 : -1;
    return 0;
  });

  // Pagination
  const totalPages = Math.ceil(sortedPlans.length / PAGE_SIZE);
  const paginatedPlans = sortedPlans.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

  const handleSort = (key: SortKey) => {
    if (sortKey === key) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortKey(key);
      setSortOrder("asc");
    }
  };

  // CSV Export
  const exportCSV = () => {
    const header = [
      "Plan Name",
      "Price",
      "Sq Ft",
      "Stories",
      "$/Sq Ft",
      "Last Updated",
      "Company",
      "Community",
      "Price Changed Recently"
    ];
    const rows = sortedPlans.map((plan) => [
      plan.plan_name,
      plan.price,
      plan.sqft,
      plan.stories,
      plan.price_per_sqft,
      plan.last_updated,
      plan.company,
      plan.community,
      plan.price_changed_recently ? "Yes" : "No"
    ]);
    const csvContent = [header, ...rows]
      .map((row) => row.map((cell) => `"${String(cell).replace(/"/g, '""')}"`).join(","))
      .join("\n");
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "plans.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-gray-50 p-0 md:p-6">
      {/* Main Card/Table */}
      <div className="w-full bg-white rounded-xl shadow p-4 md:p-8">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6 gap-4">
          <CompanyTabs companies={companies} selected={selectedCompany} onSelect={setSelectedCompany} />
          <button className="px-5 py-2 rounded-lg bg-blue-600 text-white font-semibold shadow-sm hover:bg-blue-700 transition" onClick={exportCSV}>
            Export CSV
          </button>
        </div>
        <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6 gap-4">          
          <div className="flex gap-2 items-center flex-wrap">
            <span className="text-sm font-semibold text-gray-700">Sort by:</span>
            <select
              className="border border-gray-300 rounded px-3 py-2 bg-white focus:ring-2 focus:ring-blue-400 shadow-sm text-gray-700"
              value={sortKey}
              onChange={(e) => setSortKey(e.target.value as SortKey)}
            >
              <option value="plan_name">Plan Name</option>
              <option value="price">Price</option>
              <option value="sqft">Sq Ft</option>
              <option value="last_updated">Last Updated</option>
            </select>
            <button
              className="border border-gray-300 rounded px-3 py-2 bg-gray-100 hover:bg-gray-200 font-bold shadow-sm text-gray-700"
              onClick={() => setSortOrder(sortOrder === "asc" ? "desc" : "asc")}
              title="Toggle sort order"
            >
              {sortOrder === "asc" ? "\u2191" : "\u2193"}
            </button>
          </div>
        </div>
        {loading ? (
          <Loader />
        ) : error ? (
          <ErrorMessage message={error} />
        ) : (
          <div className="overflow-x-auto rounded w-full">
            <table className="w-full min-w-full bg-white border border-gray-200 rounded shadow-sm">
              <thead className="sticky top-0 z-10">
                <tr>
                  <th className="px-4 py-3 border-b text-left text-sm font-bold text-gray-700 cursor-pointer bg-gray-100" onClick={() => handleSort("plan_name")}>Plan Name</th>
                  <th className="px-4 py-3 border-b text-left text-sm font-bold text-gray-700 cursor-pointer bg-gray-100" onClick={() => handleSort("price")}>Price</th>
                  <th className="px-4 py-3 border-b text-left text-sm font-bold text-gray-700 cursor-pointer bg-gray-100" onClick={() => handleSort("sqft")}>Sq Ft</th>
                  <th className="px-4 py-3 border-b text-left text-sm font-bold text-gray-700 bg-gray-100">Stories</th>
                  <th className="px-4 py-3 border-b text-left text-sm font-bold text-gray-700 bg-gray-100">$/Sq Ft</th>
                  <th className="px-4 py-3 border-b text-left text-sm font-bold text-gray-700 bg-gray-100">Company</th>
                  <th className="px-4 py-3 border-b text-left text-sm font-bold text-gray-700 bg-gray-100">Community</th>
                  <th className="px-4 py-3 border-b text-left text-sm font-bold text-gray-700 cursor-pointer bg-gray-100" onClick={() => handleSort("last_updated")}>Last Updated</th>
                </tr>
              </thead>
              <tbody>
                {paginatedPlans.map((plan) => (
                  <tr
                    key={plan.plan_name + plan.last_updated + plan.company}
                    className={`transition-colors duration-150 ${plan.price_changed_recently ? "bg-blue-50" : "hover:bg-gray-50"}`}
                  >
                    <td className="px-4 py-3 border-b font-semibold text-base text-gray-800">{plan.plan_name}</td>
                    <td className="px-4 py-3 border-b font-bold text-lg text-blue-700">${plan.price.toLocaleString()}</td>
                    <td className="px-4 py-3 border-b text-gray-700">{plan.sqft?.toLocaleString?.() ?? ""}</td>
                    <td className="px-4 py-3 border-b text-gray-700">{plan.stories}</td>
                    <td className="px-4 py-3 border-b text-gray-700">{plan.price_per_sqft ? `$${plan.price_per_sqft.toFixed(2)}` : ""}</td>
                    <td className="px-4 py-3 border-b flex items-center gap-2 text-gray-700">
                      {plan.company === 'DR Horton' && <span className="inline-block w-3 h-3 rounded-full bg-blue-400"></span>}
                      {plan.company === 'UnionMain Homes' && <span className="inline-block w-3 h-3 rounded-full bg-cyan-400"></span>}
                      {plan.company}
                    </td>
                    <td className="px-4 py-3 border-b text-gray-700">{plan.community}</td>
                    <td className="px-4 py-3 border-b text-xs text-gray-500">{new Date(plan.last_updated).toLocaleString()}</td>
                  </tr>
                ))}
                {paginatedPlans.length === 0 && (
                  <tr>
                    <td colSpan={8} className="text-center py-6 text-lg text-gray-500">
                      No plans found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
            <div className="mt-4 text-xs text-gray-500">
              <span className="inline-block w-3 h-3 bg-blue-200 border border-blue-300"></span>
              Highlighted rows indicate a price change in the last 24 hours.
            </div>
            {/* Pagination Controls */}
            {totalPages > 1 && (
              <div className="flex justify-center items-center gap-3 mt-6">
                <button
                  className="px-4 py-2 rounded border bg-gray-100 hover:bg-gray-200 border-gray-300 font-semibold text-gray-700"
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  disabled={page === 1}
                >
                  Prev
                </button>
                <span className="text-base font-semibold text-gray-700">
                  Page {page} of {totalPages}
                </span>
                <button
                  className="px-4 py-2 rounded border bg-gray-100 hover:bg-gray-200 border-gray-300 font-semibold text-gray-700"
                  onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                  disabled={page === totalPages}
                >
                  Next
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard; 