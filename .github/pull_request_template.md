## Skill Addition/Modification

### Skill Name
<!-- e.g., fastapi-local-dev, nextjs-routing, etc. -->

### Skill Type
- [ ] New skill
- [ ] Enhancement to existing skill
- [ ] Bug fix
- [ ] Documentation update

### Toolchain
<!-- e.g., Python/FastAPI, JavaScript/Next.js, Rust/Tauri, Universal -->

### Description
<!-- Clear description of what this skill does and why it's needed -->

### Testing
<!-- How did you test this skill? -->
- [ ] Tested with Claude Code in real project
- [ ] Verified progressive loading works
- [ ] Checked token efficiency (entry point <50 tokens)

### Checklist
- [ ] SKILL.md follows progressive disclosure format
- [ ] metadata.json is complete and valid
- [ ] No sensitive data (API keys, credentials)
- [ ] Documentation is clear and comprehensive
- [ ] Examples are provided
- [ ] Skill category is appropriate

## Self-Containment Verification

**Run these commands and paste output:**

```bash
# Verify no relative path dependencies (replace {your-skill-directory} with actual path)
grep -r "\.\\./" {your-skill-directory}/

# Expected output: (empty - no results means no relative paths found)
```

**Paste grep output here:**
```
<!-- Paste command output here. Should be empty if no ../ paths exist -->
```

**Self-Containment Checklist:**
- [ ] Zero `../` relative paths (verified above with grep command)
- [ ] Skill works in flat directory deployment
- [ ] Essential content is inlined (not just referenced)
- [ ] Complementary skills are listed informationally only (no hard dependencies)
- [ ] I have tested this skill in isolation
- [ ] No broken markdown links (all links verified)
- [ ] I have read the [SKILL_SELF_CONTAINMENT_STANDARD.md](../SKILL_SELF_CONTAINMENT_STANDARD.md)

**For reviewers:** Verify grep output is empty before approving.

### Related Issues
<!-- Link any related issues here -->

/cc @bobmatnyc
