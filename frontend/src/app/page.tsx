"use client";

import { InputModule } from "@/components/InputModule";
import { BugModule } from "@/components/BugModule";
import { NamingModule } from "@/components/NamingModule";
import { GraphModule } from "@/components/GraphModule";
import { GroupingModule } from "@/components/GroupingModule";
import { GenerationModule } from "@/components/GenerationModule";
import { useState } from "react";

export default function Home() {
  const [currentStep, setCurrentStep] = useState(1);
  const [projectData, setProjectData] = useState({
    code: "",
    language: "",
    filename: "",
    functions: [],
    services: {},
    renames: {},
  });

  const steps = [
    { id: 1, name: "Input & Analysis", icon: "📥" },
    { id: 2, name: "Bug Detection", icon: "🐛" },
    { id: 3, name: "Smart Naming", icon: "🏷️" },
    { id: 4, name: "Dependency Graph", icon: "🕸️" },
    { id: 5, name: "Service Grouping", icon: "📦" },
    { id: 6, name: "Code Generation", icon: "🚀" },
  ];

  const renderModule = () => {
    switch (currentStep) {
      case 1:
        return <InputModule
          onNext={() => setCurrentStep(2)}
          projectData={projectData}
          setProjectData={setProjectData}
        />;
      case 2:
        return <BugModule
          onNext={() => setCurrentStep(3)}
          projectData={projectData}
          setProjectData={setProjectData}
        />;
      case 3:
        return <NamingModule
          onNext={() => setCurrentStep(4)}
          projectData={projectData}
          setProjectData={setProjectData}
        />;
      case 4:
        return <GraphModule
          onNext={() => setCurrentStep(5)}
          projectData={projectData}
        />;
      case 5:
        return <GroupingModule
          onNext={() => setCurrentStep(6)}
          projectData={projectData}
          setProjectData={setProjectData}
        />;
      case 6:
        return <GenerationModule
          projectData={projectData}
        />;
      default:
        return <div>Module not found</div>;
    }
  };

  return (
    <div className="flex h-screen bg-gray-50 text-black">
      {/* Sidebar */}
      <div className="w-64 bg-white border-r border-gray-200 p-6 flex flex-col">
        <h1 className="text-xl font-bold mb-2">🧬 MicroSculpt AI</h1>
        <p className="text-sm text-gray-500 mb-6">v2.0 | Next.js Edition</p>

        <nav className="flex-1 space-y-1">
          {steps.map((step) => {
            const isActive = currentStep === step.id;
            const isCompleted = currentStep > step.id;

            return (
              <button
                key={step.id}
                onClick={() => {
                  if (step.id <= currentStep + 1) setCurrentStep(step.id);
                }}
                className={`w-full flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors ${isActive
                    ? "bg-gray-100 text-blue-600"
                    : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                  }`}
              >
                <span className="mr-3">{isCompleted ? "✅" : (isActive ? "🔵" : "⚪")}</span>
                <span>{step.name}</span>
              </button>
            );
          })}
        </nav>

        <div className="mt-auto pt-6 border-t border-gray-100">
          <div className="bg-blue-50 p-4 rounded-lg">
            <p className="text-xs text-blue-800">
              💡 <strong>Pro Tip:</strong> Use AI suggestions in Steps 2 & 3 for best results!
            </p>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto p-8">
        <div className="max-w-5xl mx-auto">
          {renderModule()}
        </div>
      </div>
    </div>
  );
}
