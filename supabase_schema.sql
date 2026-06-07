-- Create extension for UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =========================================================
-- 1. Campaigns Table (Facebook Ads / TikTok)
-- =========================================================
CREATE TABLE campaigns (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    platform VARCHAR(50) NOT NULL, -- e.g., 'Facebook', 'TikTok'
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- =========================================================
-- 2. Ad Metrics Table (Layer 1 - Traffic)
-- Stores daily aggregated performance from Ads
-- =========================================================
CREATE TABLE ad_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    date DATE NOT NULL,
    campaign_id UUID REFERENCES campaigns(id),
    ad_spend DECIMAL(12, 2) NOT NULL DEFAULT 0,
    reach INTEGER NOT NULL DEFAULT 0,
    impressions INTEGER NOT NULL DEFAULT 0,
    engagements INTEGER NOT NULL DEFAULT 0,
    messages INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    UNIQUE(date, campaign_id)
);

-- =========================================================
-- 3. Leads & CRM Table (Layer 2, 3, 4 - Chat to Sales)
-- Stores individual lead progress from OhoChat to JUBILI
-- =========================================================
CREATE TABLE leads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_name VARCHAR(255),
    source VARCHAR(50) NOT NULL, -- e.g., 'OhoChat-FB', 'Organic'
    phone VARCHAR(50),
    line_id VARCHAR(100),
    
    -- Funnel Status (Crucial for Pipeline tracking)
    status VARCHAR(50) NOT NULL DEFAULT 'chat_inbound', 
    -- Valid statuses: chat_inbound, qualified, lead_passed, negotiation, quotation, closed_won, closed_lost
    
    -- SLA Tracking
    first_response_time_mins INTEGER, 
    
    -- Revenue Data
    expected_revenue DECIMAL(12, 2) DEFAULT 0,
    actual_revenue DECIMAL(12, 2) DEFAULT 0,
    
    assigned_sales_rep VARCHAR(100),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- =========================================================
-- 4. AI Insights Table (Layer 5)
-- n8n will push weekly AI summaries here
-- =========================================================
CREATE TABLE ai_insights (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    analysis_date DATE NOT NULL,
    insight_type VARCHAR(50), -- e.g., 'bottleneck', 'opportunity', 'weekly_summary'
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- =========================================================
-- Enable Row Level Security (RLS) for security best practices
-- =========================================================
ALTER TABLE campaigns ENABLE ROW LEVEL SECURITY;
ALTER TABLE ad_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_insights ENABLE ROW LEVEL SECURITY;

-- Create basic access policies (Allow authenticated APIs to read/write)
CREATE POLICY "Allow public read access" ON campaigns FOR SELECT USING (true);
CREATE POLICY "Allow public read access" ON ad_metrics FOR SELECT USING (true);
CREATE POLICY "Allow public read access" ON leads FOR SELECT USING (true);
CREATE POLICY "Allow public read access" ON ai_insights FOR SELECT USING (true);

-- API keys (service_role) used by n8n will naturally bypass RLS to insert/update data.
