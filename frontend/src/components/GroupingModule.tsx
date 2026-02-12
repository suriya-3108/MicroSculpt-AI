import { useState } from 'react';
import { Package, Layers, ChevronRight, Loader2, ArrowRight } from 'lucide-react';

interface GroupingModuleProps {
    onNext: () => void;
    projectData: any;
    setProjectData: (data: any) => void;
}

export function GroupingModule({ onNext, projectData, setProjectData }: GroupingModuleProps) {
    const [loading, setLoading] = useState(false);
    const [services, setServices] = useState<Record<string, string[]>>({});

    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

    const groupServices = async () => {
        setLoading(true);
        try {
            const response = await fetch(`${API_URL}/group-services`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    functions: projectData.functions
                }),
            });

            const data = await response.json();

            if (data.error) {
                alert("Error: " + data.error);
            } else {
                setServices(data.services);
                setProjectData({ ...projectData, services: data.services });
            }
        } catch (e) {
            console.error(e);
            alert("Failed to connect to API");
        } finally {
            setLoading(false);
        }
    };

    const proceed = () => {
        if (Object.keys(services).length === 0) {
            alert("Please group services first.");
            return;
        }
        setProjectData({ ...projectData, services });
        onNext();
    };

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="border-b pb-4">
                <h2 className="text-2xl font-bold flex items-center">
                    <span className="bg-black text-white rounded-full w-8 h-8 flex items-center justify-center text-sm mr-3">5</span>
                    Service Grouping
                </h2>
                <p className="text-gray-500 mt-1 ml-11">AI-powered microservice clustering.</p>
            </div>

            {Object.keys(services).length === 0 ? (
                <div className="bg-white border rounded-xl p-12 text-center">
                    <Layers className="w-16 h-16 text-gray-200 mx-auto mb-6" />
                    <h3 className="text-xl font-bold text-gray-900 mb-2">Group into Microservices</h3>
                    <p className="text-gray-500 mb-8 max-w-md mx-auto">
                        We use TF-IDF and K-Means clustering to logically group your functions into separate services.
                    </p>
                    <button
                        onClick={groupServices}
                        disabled={loading}
                        className="bg-blue-600 text-white px-8 py-3 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 flex items-center mx-auto"
                    >
                        {loading ? <Loader2 className="w-5 h-5 mr-2 animate-spin" /> : <Package className="w-5 h-5 mr-2" />}
                        {loading ? "Grouping..." : "Generate Service Groups"}
                    </button>
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {Object.entries(services).map(([svcName, funcs]: [string, any], i) => (
                        <div key={i} className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm hover:shadow-md transition-shadow">
                            <div className="flex items-center mb-4">
                                <div className={`p-2 rounded-lg mr-3 ${['bg-red-50', 'bg-blue-50', 'bg-green-50', 'bg-purple-50'][i % 4]}`}>
                                    <Layers className={`w-5 h-5 ${['text-red-500', 'text-blue-500', 'text-green-500', 'text-purple-500'][i % 4]}`} />
                                </div>
                                <h3 className="font-bold text-lg">{svcName}</h3>
                            </div>

                            <div className="bg-gray-50 rounded-lg p-3 min-h-[150px]">
                                <p className="text-xs font-semibold text-gray-500 uppercase mb-2">Functions ({funcs.length})</p>
                                <ul className="space-y-1">
                                    {funcs.map((func: string, j: number) => (
                                        <li key={j} className="text-sm px-2 py-1 bg-white border rounded shadow-sm flex items-center">
                                            <ChevronRight className="w-3 h-3 mr-1 text-gray-400" />
                                            {func}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {Object.keys(services).length > 0 && (
                <div className="flex justify-end pt-6">
                    <button
                        onClick={proceed}
                        className="bg-black text-white px-8 py-3 rounded-lg font-medium hover:bg-gray-800 flex items-center"
                    >
                        Confirm Structure & Continue
                        <ArrowRight className="w-5 h-5 ml-2" />
                    </button>
                </div>
            )}
        </div>
    );
}
