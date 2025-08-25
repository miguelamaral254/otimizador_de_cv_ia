import React from 'react';
import { Link } from 'react-router-dom';

const About = () => {
    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
            {/* Hero Section */}
            <section className="py-20">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center">
                        <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
                            Sobre o <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">CV Genius</span>
                        </h1>
                        <p className="text-xl md:text-2xl text-gray-600 max-w-3xl mx-auto">
                            Transformando carreiras através da inteligência artificial e análise inteligente de currículos.
                        </p>
                    </div>
                </div>
            </section>

            {/* Missão e Visão */}
            <section className="py-20 bg-white">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="grid md:grid-cols-2 gap-16 items-center">
                        <div>
                            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
                                Nossa Missão
                            </h2>
                            <p className="text-lg text-gray-600 mb-6">
                                Democratizar o acesso a ferramentas avançadas de otimização de currículos,
                                permitindo que profissionais de todos os níveis possam se destacar no mercado de trabalho.
                            </p>
                            <p className="text-lg text-gray-600">
                                Acreditamos que cada pessoa merece a oportunidade de apresentar seu melhor
                                perfil profissional de forma eficaz e estratégica.
                            </p>
                        </div>
                        <div className="text-center">
                            <div className="w-64 h-64 bg-gradient-to-br from-blue-100 to-purple-100 rounded-full flex items-center justify-center mx-auto">
                                <svg className="w-32 h-32 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                                </svg>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* História */}
            <section className="py-20 bg-gray-50">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                            Nossa História
                        </h2>
                        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                            Desde 2024, estamos comprometidos em revolucionar a forma como as pessoas
                            apresentam suas qualificações profissionais.
                        </p>
                    </div>

                    <div className="grid md:grid-cols-3 gap-8">
                        <div className="text-center">
                            <div className="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-6 text-white text-2xl font-bold">
                                1
                            </div>
                            <h3 className="text-xl font-semibold text-gray-900 mb-2">Início</h3>
                            <p className="text-gray-600">
                                Identificamos a necessidade de uma ferramenta inteligente para otimização
                                de currículos no mercado brasileiro.
                            </p>
                        </div>
                        <div className="text-center">
                            <div className="w-20 h-20 bg-purple-600 rounded-full flex items-center justify-center mx-auto mb-6 text-white text-2xl font-bold">
                                2
                            </div>
                            <h3 className="text-xl font-semibold text-gray-900 mb-2">Desenvolvimento</h3>
                            <p className="text-gray-600">
                                Desenvolvemos uma solução baseada em IA que analisa vagas e otimiza
                                currículos automaticamente.
                            </p>
                        </div>
                        <div className="text-center">
                            <div className="w-20 h-20 bg-green-600 rounded-full flex items-center justify-center mx-auto mb-6 text-white text-2xl font-bold">
                                3
                            </div>
                            <h3 className="text-xl font-semibold text-gray-900 mb-2">Crescimento</h3>
                            <p className="text-gray-600">
                                Expandimos nossa plataforma para atender milhares de profissionais
                                em todo o Brasil.
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Tecnologia */}
            <section className="py-20 bg-white">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="grid md:grid-cols-2 gap-16 items-center">
                        <div className="text-center">
                            <div className="w-64 h-64 bg-gradient-to-br from-purple-100 to-pink-100 rounded-full flex items-center justify-center mx-auto">
                                <svg className="w-32 h-32 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                                </svg>
                            </div>
                        </div>
                        <div>
                            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
                                Tecnologia de Ponta
                            </h2>
                            <p className="text-lg text-gray-600 mb-6">
                                Utilizamos as mais avançadas tecnologias de inteligência artificial,
                                incluindo processamento de linguagem natural e machine learning.
                            </p>
                            <div className="space-y-4">
                                <div className="flex items-center">
                                    <svg className="w-6 h-6 text-green-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                    </svg>
                                    <span className="text-gray-700">Análise inteligente de vagas</span>
                                </div>
                                <div className="flex items-center">
                                    <svg className="w-6 h-6 text-green-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                    </svg>
                                    <span className="text-gray-700">Processamento de linguagem natural</span>
                                </div>
                                <div className="flex items-center">
                                    <svg className="w-6 h-6 text-green-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                    </svg>
                                    <span className="text-gray-700">Machine learning avançado</span>
                                </div>
                                <div className="flex items-center">
                                    <svg className="w-6 h-6 text-green-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                    </svg>
                                    <span className="text-gray-700">Análise de compatibilidade em tempo real</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Equipe */}
            <section className="py-20 bg-gray-50">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                            Nossa Equipe
                        </h2>
                        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                            Profissionais apaixonados por tecnologia e inovação,
                            comprometidos em transformar a experiência de busca por emprego.
                        </p>
                    </div>

                    <div className="grid md:grid-cols-3 gap-8">
                        <div className="text-center">
                            <div className="w-32 h-32 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full mx-auto mb-4"></div>
                            <h3 className="text-xl font-semibold text-gray-900 mb-2">Desenvolvedores</h3>
                            <p className="text-gray-600">
                                Especialistas em IA, machine learning e desenvolvimento web,
                                criando soluções inovadoras e escaláveis.
                            </p>
                        </div>
                        <div className="text-center">
                            <div className="w-32 h-32 bg-gradient-to-br from-purple-400 to-purple-600 rounded-full mx-auto mb-4"></div>
                            <h3 className="text-xl font-semibold text-gray-900 mb-2">Especialistas em RH</h3>
                            <p className="text-gray-600">
                                Profissionais com vasta experiência em recrutamento e seleção,
                                garantindo a relevância das análises.
                            </p>
                        </div>
                        <div className="text-center">
                            <div className="w-32 h-32 bg-gradient-to-br from-green-400 to-green-600 rounded-full mx-auto mb-4"></div>
                            <h3 className="text-xl font-semibold text-gray-900 mb-2">Designers UX/UI</h3>
                            <p className="text-gray-600">
                                Criadores de experiências intuitivas e agradáveis,
                                focados na usabilidade e satisfação do usuário.
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
                <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
                    <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
                        Pronto para transformar sua carreira?
                    </h2>
                    <p className="text-xl text-blue-100 mb-8">
                        Junte-se a milhares de profissionais que já otimizaram seus currículos com IA.
                    </p>
                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        <Link
                            to="/register"
                            className="bg-white text-blue-600 hover:bg-gray-100 px-8 py-4 rounded-lg text-lg font-semibold transition-all transform hover:scale-105 shadow-lg"
                        >
                            Começar Gratuitamente
                        </Link>
                        <Link
                            to="/contact"
                            className="border-2 border-white text-white hover:bg-white hover:text-blue-600 px-8 py-4 rounded-lg text-lg font-semibold transition-all transform hover:scale-105"
                        >
                            Falar Conosco
                        </Link>
                    </div>
                </div>
            </section>
        </div>
    );
};

export default About;
