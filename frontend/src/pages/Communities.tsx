import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Loader from "../components/Loader";
import ErrorMessage from "../components/ErrorMessage";
import API_URL from '../config';
import { getCompanyColor } from '../utils/colors';

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

interface Community {
  name: string;
  companies: string[];
  totalPlans: number;
  totalNow: number;
  avgPrice: number;
  priceRange: { min: number; max: number };
  recentChanges: number;
}

const Communities: React.FC = () => {
  const [communities, setCommunities] = useState<Community[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const fetchCommunities = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch(API_URL + "/plans");
      if (!res.ok) throw new Error("Failed to fetch plans");
      const plans: Plan[] = await res.json();
      
      // Group plans by community
      const communityMap = new Map<string, Plan[]>();
      plans.forEach(plan => {
        if (!communityMap.has(plan.community)) {
          communityMap.set(plan.community, []);
        }
        communityMap.get(plan.community)!.push(plan);
      });

      // Convert to Community objects
      const communityData: Community[] = Array.from(communityMap.entries()).map(([name, plans]) => {
        const companies = Array.from(new Set(plans.map(p => p.company)));
        const prices = plans.map(p => p.price).filter(p => p > 0);
        const recentChanges = plans.filter(p => p.price_changed_recently).length;
        const totalPlans = plans.filter(p => p.type === 'plan').length;
        const totalNow = plans.filter(p => p.type === 'now').length;
        
        return {
          name,
          companies,
          totalPlans,
          totalNow,
          avgPrice: prices.length > 0 ? Math.round(prices.reduce((a, b) => a + b, 0) / prices.length) : 0,
          priceRange: {
            min: prices.length > 0 ? Math.min(...prices) : 0,
            max: prices.length > 0 ? Math.max(...prices) : 0
          },
          recentChanges
        };
      });

      setCommunities(communityData);
    } catch (err: any) {
      setError(err.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCommunities();
    const interval = setInterval(fetchCommunities, 60 * 1000); // Refresh every 1 min
    return () => clearInterval(interval);
  }, []);

  const handleCommunityClick = (communityName: string) => {
    navigate(`/community/${encodeURIComponent(communityName)}`);
  };

  if (loading) return <Loader />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto p-4 md:p-8 lg:p-12">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Communities</h1>
          <p className="text-gray-600">Explore home plans by community</p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-12">
          {communities.map((community) => (
            <div
              key={community.name}
              onClick={() => handleCommunityClick(community.name)}
              className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer transform hover:scale-105"
            >
                             <div className="relative h-48 rounded-t-xl overflow-hidden">
                 <img
                                       src={
                      community.name === 'Cambridge' ? 'https://lh3.googleusercontent.com/p/AF1QipNy23uJq2nst_j1A4fK5_S63FLs03bYz8cReUv8=s680-w680-h510-rw' :
                      community.name === 'Milrany' ? 'https://unionmainhomes.com/wp-content/uploads/2024/08/42_3504_Thomas_Earl_Way_Melissa_TX_75454__Exports12-1.jpg' :
                      community.name === 'Brookville' ? 'https://nhs-dynamic-secure.akamaized.net/images/homes/union56526/94853826-250522.jpg?encoder=freeimage&progressive=true&maxwidth=1932&format=jpg' :
                      community.name === 'Edgewater' ? 'https://unionmainhomes.com/wp-content/uploads/2022/05/02-Sign-2.jpg' :
                      community.name === 'Creekside' ? 'https://ssl.cdn-redfin.com/photo/community/30443754/mbphoto/genMid.0_4.jpg' :
                      'https://elevontx.com/wp-content/uploads/2024/01/UnionMain50Model.jpeg.webp'
                    }
                   alt={community.name}
                   className="w-full h-full object-cover"
                 />
                {community.recentChanges > 0 && (
                  <div className="absolute top-3 right-3 bg-red-500 text-white text-xs font-bold px-2 py-1 rounded-full">
                    {community.recentChanges} new
                  </div>
                )}
              </div>
              
              <div className="p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4">{community.name}</h3>
                
                <div className="space-y-4">
                  {/* Plan/Now Summary */}
                  <div className="flex justify-between items-center bg-gray-50 rounded-lg p-3">
                    <div className="flex items-center gap-2">
                      <span className="inline-block w-3 h-3 rounded-full bg-purple-500"></span>
                      <span className="text-sm font-medium text-gray-700">Plans</span>
                    </div>
                    <span className="font-bold text-purple-600">{community.totalPlans}</span>
                  </div>
                  
                  <div className="flex justify-between items-center bg-gray-50 rounded-lg p-3">
                    <div className="flex items-center gap-2">
                      <span className="inline-block w-3 h-3 rounded-full bg-green-500"></span>
                      <span className="text-sm font-medium text-gray-700">Available Now</span>
                    </div>
                    <span className="font-bold text-green-600">{community.totalNow}</span>
                  </div>
                  
                  {/* Price Info */}
                  <div className="border-t pt-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm text-gray-600">Avg Price:</span>
                      <span className="font-semibold text-blue-600">
                        ${community.avgPrice.toLocaleString()}
                      </span>
                    </div>
                    
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-sm text-gray-600">Price Range:</span>
                      <span className="font-semibold text-gray-900 text-sm">
                        ${community.priceRange.min.toLocaleString()} - ${community.priceRange.max.toLocaleString()}
                      </span>
                    </div>
                  </div>
                  
                  {/* Builders */}
                  <div className="border-t pt-4">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Builders:</span>
                      <div className="flex gap-1">
                        {community.companies.slice(0, 3).map((company) => {
                          const color = getCompanyColor(company);
                          return (
                            <span
                              key={company}
                              className="inline-block w-3 h-3 rounded-full border"
                              style={{ backgroundColor: color, borderColor: color }}
                              title={company}
                            />
                          );
                        })}
                        {community.companies.length > 3 && (
                          <span className="text-xs text-gray-500">+{community.companies.length - 3}</span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        {communities.length === 0 && (
          <div className="text-center py-12">
            <p className="text-lg text-gray-500">No communities found.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Communities; 