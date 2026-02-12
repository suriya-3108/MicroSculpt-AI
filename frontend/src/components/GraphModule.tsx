import { useState, useEffect } from 'react';
import { Network, Activity, GitFork, Loader2 } from 'lucide-react';
import Image from 'next/image';

interface GraphModuleProps {
    onNext: () => void;
    projectData: any;
}

export function GraphModule({ onNext, projectData }: GraphModuleProps) {
    const [loading, setLoading] = useState(false);
    const [graphImage, setGraphImage] = useState<string | null>(null);
    const [metrics, setMetrics] = useState<any>(null);

    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

    useEffect(() => {
        generateGraph();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    const generateGraph = async () => {
        setLoading(true);
        try {
            const response = await fetch(`${API_URL}/dependency-graph`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    functions: projectData.functions
                }),
            });

            const data = await response.json();

            if (data.error) {
                // Handle error silently or show toast
                console.error(data.error);
            } else {
                setGraphImage(data.image);
                setMetrics(data.metrics);
            }
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="border-b pb-4">
                <h2 className="text-2xl font-bold flex items-center">
                    <span className="bg-black text-white rounded-full w-8 h-8 flex items-center justify-center text-sm mr-3">4</span>
                    Dependency Graph
                </h2>
                <p className="text-gray-500 mt-1 ml-11">Visualizing function interdependencies.</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Metrics */}
                <div className="col-span-1 space-y-4">
                    <div className="bg-white border p-6 rounded-xl flex items-center space-x-4 shadow-sm">
                        <div className="bg-blue-50 p-3 rounded-full"><Activity className="w-6 h-6 text-blue-600" /></div>
                        <div>
                            <h4 className="text-2xl font-bold">{metrics?.total_functions || 0}</h4>
                            <p className="text-sm text-gray-500">Total Functions</p>
                        </div>
                    </div>

                    <div className="bg-white border p-6 rounded-xl flex items-center space-x-4 shadow-sm">
                        <div className="bg-purple-50 p-3 rounded-full"><Network className="w-6 h-6 text-purple-600" /></div>
                        <div>
                            <h4 className="text-2xl font-bold">{metrics?.connections || 0}</h4>
                            <p className="text-sm text-gray-500">Connections</p>
                        </div>
                    </div>

                    <div className="bg-white border p-6 rounded-xl flex items-center space-x-4 shadow-sm">
                        <div className="bg-orange-50 p-3 rounded-full"><GitFork className="w-6 h-6 text-orange-600" /></div>
                        <div>
                            <h4 className="text-2xl font-bold">{metrics?.isolated || 0}</h4>
                            <p className="text-sm text-gray-500">Isolated Nodes</p>
                        </div>
                    </div>
                </div>

                {/* Graph Image */}
                <div className="col-span-2 bg-white border rounded-xl p-4 flex items-center justify-center min-h-[400px] shadow-sm relative">
                    {loading ? (
                        <div className="flex flex-col items-center">
                            <Loader2 className="w-8 h-8 animate-spin text-gray-400 mb-2" />
                            <p className="text-gray-500">Generating visualization...</p>
                        </div>
                    ) : graphImage ? (
                        <img
                            src={`data:image/png;base64,${graphImage}`}
                            alt="Dependency Graph"
                            className="w-full h-auto object-contain max-h-[500px]"
                        />
                    ) : (
                        <p className="text-gray-400">No graph data available</p>
                    )}
                </div>
            </div>

            <div className="flex justify-end pt-4">
                <button
                    onClick={onNext}
                    className="bg-black text-white px-8 py-3 rounded-lg font-medium hover:bg-gray-800 transition-all"
                >
                    Continue to Grouping
                </button>
            </div>
        </div>
    );
}
