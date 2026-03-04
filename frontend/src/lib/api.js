import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8088';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const getExecutiveDashboard = async (tenantSlug = 'default') => {
    try {
        const response = await api.get(`/api/v1/dashboard/executive/${tenantSlug}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching dashboard data:', error);
        throw error;
    }
};

export default api;
