CREATE INDEX cms_knowledge_sources_approved_tag_version_index
    ON cms_knowledge_sources (applicable_tag, canonical_id, effective_version DESC)
    WHERE approval_state = 'approved';