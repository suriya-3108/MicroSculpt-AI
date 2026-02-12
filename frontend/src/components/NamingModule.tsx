import { useState } from 'react';
import { Tag, Check, ArrowRight, Loader2, RefreshCw } from 'lucide-react';

interface NamingModuleProps {
    onNext: () => void;
    projectData: any;
    setProjectData: (data: any) => void;
}

export function NamingModule({ onNext, projectData, setProjectData }: NamingModuleProps) {
    const [loading, setLoading] = useState(false);
    const [suggestions, setSuggestions] = useState<any[]>([]);
    const [accepted, setAccepted] = useState<Record<string, string>>({});

    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

    const analyzeNames = async () => {
        setLoading(true);
        try {
            const funcNames = projectData.functions.map((f: any) => f.name);

            const response = await fetch(`${API_URL}/suggest-names`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    code: projectData.code,
                    language: projectData.language,
                    functions: funcNames
                }),
            });

            const data = await response.json();

            if (data.error) {
                alert("Error: " + data.error);
            } else {
                setSuggestions(data.suggestions || []);
            }
        } catch (e) {
            console.error(e);
            alert("Failed to connect to API");
        } finally {
            setLoading(false);
        }
    };

    const toggleAccept = (current: string, newName: string) => {
        setAccepted(prev => {
            const next = { ...prev };
            if (next[current]) {
                delete next[current];
            } else {
                next[current] = newName;
            }
            return next;
        });
    };

    const applyRenames = () => {
        // Update code via simple replace (in a real app, use AST transformation on backend)
        let newCode = projectData.code;
        const renames = { ...projectData.renames, ...accepted };

        // Sort by length desc to avoid substring issues
        const sortedRenames = Object.entries(accepted).sort((a, b) => b[0].length - a[0].length);

        for (const [oldName, newName] of sortedRenames) {
            // Simple regex replace to match function calls and defs
            // This is fragile but matches original Streamlit logic
            const regex = new RegExp(`\\b${oldName}\\b`, 'g');
            newCode = newCode.replace(regex, newName);
        }

        const updatedFunctions = projectData.functions.map((f: any) => ({
            ...f,
            name: accepted[f.name] || f.name
        }));

        setProjectData({
            ...projectData,
            code: newCode,
            functions: updatedFunctions,
            renames: renames
        });

        alert(`Applied ${Object.keys(accepted).length} renames.`);
        onNext();
    };

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="border-b pb-4">
                <h2 className="text-2xl font-bold flex items-center">
                    <span className="bg-black text-white rounded-full w-8 h-8 flex items-center justify-center text-sm mr-3">3</span>
                    Smart Function Naming
                </h2>
                <p className="text-gray-500 mt-1 ml-11">Let AI suggest descriptive names for your functions.</p>
            </div>

            <div className="bg-white border border-gray-200 rounded-xl p-6">
                {suggestions.length === 0 ? (
                    <div className="text-center py-12">
                        <Tag className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                        <h3 className="text-lg font-medium text-gray-900 mb-2">Analyze Function Names</h3>
                        <p className="text-gray-500 mb-6">Detect generic names like "func1" or "process_data" and replace them.</p>
                        <button
                            onClick={analyzeNames}
                            disabled={loading}
                            className="bg-black text-white px-6 py-2 rounded-lg font-medium hover:bg-gray-800 disabled:opacity-50 flex items-center mx-auto"
                        >
                            {loading ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : <RefreshCw className="w-4 h-4 mr-2" />}
                            {loading ? "Analyzing..." : "Start Analysis"}
                        </button>
                    </div>
                ) : (
                    <div>
                        <div className="flex justify-between items-center mb-4">
                            <h3 className="font-bold">Suggestions ({suggestions.length})</h3>
                            <div className="text-sm text-gray-500">
                                Select suggestions to apply
                            </div>
                        </div>

                        <div className="space-y-3 max-h-[400px] overflow-auto mb-6 pr-2">
                            {suggestions.map((s: any, i: number) => (
                                <div key={i}
                                    onClick={() => toggleAccept(s.current, s.suggested)}
                                    className={`p-4 rounded-lg border cursor-pointer transition-all flex items-center justify-between
                            ${accepted[s.current] ? 'border-green-500 bg-green-50 ring-1 ring-green-500' : 'border-gray-200 hover:border-blue-300'}`}
                                >
                                    <div className="flex-1">
                                        <div className="flex items-center space-x-3 mb-1">
                                            <span className="font-mono text-red-500 line-through text-sm">{s.current}</span>
                                            <ArrowRight className="w-4 h-4 text-gray-400" />
                                            <span className="font-mono text-green-700 font-bold">{s.suggested}</span>
                                        </div>
                                        <p className="text-xs text-gray-500">{s.reason}</p>
                                    </div>
                                    <div className={`w-6 h-6 rounded-full border flex items-center justify-center
                                ${accepted[s.current] ? 'bg-green-500 border-green-500' : 'border-gray-300 bg-white'}`}>
                                        {accepted[s.current] && <Check className="w-4 h-4 text-white" />}
                                    </div>
                                </div>
                            ))}
                        </div>

                        <button
                            onClick={applyRenames}
                            className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 flex items-center justify-center"
                        >
                            Apply Selected & Continue
                        </button>
                    </div>
                )}
            </div>

            {suggestions.length > 0 && (
                <div className="flex justify-end">
                    <button onClick={onNext} className="text-sm text-gray-500 hover:text-gray-900 underline">
                        Skip naming
                    </button>
                </div>
            )}
        </div>
    );
}
