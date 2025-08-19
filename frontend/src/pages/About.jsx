import React from 'react'

function About() {
    return (
        <div className="container mx-auto px-4 py-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-6">Sobre o Projeto</h1>
            <div className="max-w-4xl">
                <p className="text-lg text-gray-600 mb-6">
                    O "Otimizador de Currículos com IA" é um projeto desafiador que visa criar uma plataforma
                    completa para análise e otimização de currículos usando inteligência artificial.
                </p>

                <h2 className="text-2xl font-semibold text-gray-900 mb-4">Objetivos do Desafio</h2>
                <ul className="list-disc list-inside text-gray-600 mb-6 space-y-2">
                    <li>Implementar sistema de upload de arquivos PDF</li>
                    <li>Integrar APIs de IA para análise de texto</li>
                    <li>Criar dashboard com métricas e visualizações</li>
                    <li>Implementar sistema de autenticação</li>
                    <li>Desenvolver histórico de versões</li>
                </ul>

                <h2 className="text-2xl font-semibold text-gray-900 mb-4">Tecnologias Utilizadas</h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="text-center p-3 bg-gray-100 rounded-lg">
                        <span className="font-medium text-gray-800">React</span>
                    </div>
                    <div className="text-center p-3 bg-gray-100 rounded-lg">
                        <span className="font-medium text-gray-800">Tailwind CSS</span>
                    </div>
                    <div className="text-center p-3 bg-gray-100 rounded-lg">
                        <span className="font-medium text-gray-800">Vite</span>
                    </div>
                    <div className="text-center p-3 bg-gray-100 rounded-lg">
                        <span className="font-medium text-gray-800">JavaScript</span>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default About
