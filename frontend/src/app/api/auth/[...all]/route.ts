import { auth } from '@/lib/auth';
import { headers } from 'next/headers';
import { NextRequest } from 'next/server';

export const { GET, POST } = auth;

export async function handler(req: NextRequest) {
  const response = await auth.handler(req);
  return response;
}
