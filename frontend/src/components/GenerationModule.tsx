import { useState } from 'react';
import { Download, Code, CheckCircle, FileCode, Server, Database } from 'lucide-react';

interface GenerationModuleProps {
    projectData: any;
}

export function GenerationModule({ projectData }: GenerationModuleProps) {
    const [loading, setLoading] = useState(false);
    const [language, setLanguage] = useState<'python' | 'javascript'>('python');

    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

    const generateCode = async () => {
        setLoading(true);
        try {
            const response = await fetch(`${API_URL}/generate-code`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    services: projectData.services,
                    language: language,
                    functions: projectData.functions,
                    renames: projectData.renames,
                    filename: projectData.filename,
                    source_code: projectData.code  // Pass original code for import extraction
                }),
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `microservices_${language}.zip`;
                document.body.appendChild(a);
                a.click();
                a.remove();
            } else {
                const data = await response.json();
                alert("Error: " + (data.error || "Generation failed"));
            }
        } catch (e) {
            console.error(e);
            alert("Failed to connect to API");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="border-b pb-4">
                <h2 className="text-2xl font-bold flex items-center">
                    <span className="bg-black text-white rounded-full w-8 h-8 flex items-center justify-center text-sm mr-3">6</span>
                    Code Generation
                </h2>
                <p className="text-gray-500 mt-1 ml-11">Generate production-ready microservices.</p>
            </div>

            <div className="bg-white border rounded-xl p-8 mb-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div>
                        <h3 className="text-lg font-bold mb-4">Configuration</h3>

                        <div className="mb-6">
                            <label className="block text-sm font-medium text-gray-700 mb-2">Target Language</label>
                            <div className="grid grid-cols-2 gap-4">
                                <button
                                    onClick={() => setLanguage('python')}
                                    className={`p-4 border rounded-lg flex flex-col items-center justify-center text-center transition-all
                            ${language === 'python' ? 'border-blue-500 bg-blue-50 ring-1 ring-blue-500' : 'border-gray-200 hover:border-gray-300'}`}
                                >
                                    <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" className="w-8 h-8 mb-2" alt="Python" />
                                    <span className="text-sm font-medium">Python (Flask)</span>
                                </button>

                                <button
                                    onClick={() => setLanguage('javascript')}
                                    className={`p-4 border rounded-lg flex flex-col items-center justify-center text-center transition-all
                            ${language === 'javascript' ? 'border-yellow-500 bg-yellow-50 ring-1 ring-yellow-500' : 'border-gray-200 hover:border-gray-300'}`}
                                >
                                    <img src="https://upload.wikimedia.org/wikipedia/commons/6/6a/JavaScript-logo.png" className="w-8 h-8 mb-2" alt="JS" />
                                    <span className="text-sm font-medium">Node.js (Express)</span>
                                </button>
                            </div>
                        </div>

                        <div className="bg-gray-50 rounded-lg p-4">
                            <h4 className="text-xs font-bold text-gray-500 uppercase mb-3">Included in Package</h4>
                            <ul className="space-y-2 text-sm">
                                <li className="flex items-center text-gray-700">
                                    <Server className="w-4 h-4 mr-2 text-gray-400" />
                                    Microservice API Code
                                </li>
                                <li className="flex items-center text-gray-700">
                                    <FileCode className="w-4 h-4 mr-2 text-gray-400" />
                                    Dockerfiles per Service
                                </li>
                                <li className="flex items-center text-gray-700">
                                    <Database className="w-4 h-4 mr-2 text-gray-400" />
                                    docker-compose.yml
                                </li>
                                <li className="flex items-center text-gray-700">
                                    <CheckCircle className="w-4 h-4 mr-2 text-gray-400" />
                                    README & Documentation
                                </li>
                            </ul>
                        </div>
                    </div>

                    <div className="flex flex-col items-center justify-center border-l border-gray-100 pl-8">
                        <div className="text-center mb-8">
                            <h3 className="text-2xl font-bold mb-2">Ready to Launch</h3>
                            <p className="text-gray-500">
                                Your code has been analyzed, cleaned, and architecturalized.<br />
                                Click below to download your new system.
                            </p>
                        </div>

                        <button
                            onClick={generateCode}
                            disabled={loading}
                            className="w-full max-w-sm bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-8 py-4 rounded-xl font-bold shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all flex items-center justify-center"
                        >
                            {loading ? (
                                <>
                                    <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin mr-3"></div>
                                    Packaging System...
                                </>
                            ) : (
                                <>
                                    <Download className="w-6 h-6 mr-3" />
                                    Download Microservices
                                </>
                            )}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
