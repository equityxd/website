import type { APIRoute } from 'astro';
import fs from 'node:fs/promises';
import path from 'node:path';

// Path to the JSON file
const dataPath = path.join(process.cwd(), 'src/data/portfolio.json');

export const GET: APIRoute = async () => {
    try {
        const data = await fs.readFile(dataPath, 'utf-8');
        return new Response(data, {
            status: 200,
            headers: {
                "Content-Type": "application/json"
            }
        });
    } catch (error: any) {
        return new Response(JSON.stringify({ error: 'Failed to read data', details: error.message }), { status: 500 });
    }
}

export const POST: APIRoute = async ({ request }) => {
    try {
        const body = await request.json();

        // Safety check: Ensure the body has the expected structure
        if (!body.profile || !body.experience) {
            return new Response(JSON.stringify({ error: 'Invalid data structure' }), { status: 400 });
        }

        // Write back to the file
        await fs.writeFile(dataPath, JSON.stringify(body, null, 4), 'utf-8');

        return new Response(JSON.stringify({ success: true, message: 'Saved successfully' }), {
            status: 200,
            headers: {
                "Content-Type": "application/json"
            }
        });
    } catch (error: any) {
        console.error(error);
        return new Response(JSON.stringify({ error: 'Failed to save data', details: error.message }), { status: 500 });
    }
}
