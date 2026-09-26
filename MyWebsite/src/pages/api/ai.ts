import type { APIRoute } from 'astro';

export const POST: APIRoute = async ({ request }) => {
    try {
        const body = await request.json();
        const { prompt, currentText } = body;

        // TODO: Connect to Real LLM (OpenAI/Gemini).
        // For now, we simulate a response based on the prompt.
        // This allows the UI flow to be tested and verified.

        let suggestion = "";
        if (prompt.includes("professional")) {
            suggestion = "I am a strategic leader with over 15 years of experience in driving finance transformation and operational excellence. My expertise lies in bridging the gap between complex data and actionable business insights.";
        } else if (prompt.includes("shorter")) {
            suggestion = "Strategic finance leader specializing in data-driven operational excellence and automation.";
        } else {
            suggestion = `[AI Suggestion based on "${prompt}"]: This is a refined version of your text focusing on impact and clarity.`;
        }

        return new Response(JSON.stringify({ suggestion }), {
            status: 200,
            headers: { "Content-Type": "application/json" }
        });

    } catch (error) {
        return new Response(JSON.stringify({ error: 'Failed to generate text' }), { status: 500 });
    }
}
