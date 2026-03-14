# Brand Images - AI Image Generation Project

**Last Updated:** March 12, 2026 (1:15 AM)  
**Status:** Planning phase - deciding between cloud vs local generation

## What This Is
Set up AI image generation for creating brand ad images (logos, social media banners, product photos, etc.)

## Session Summary: March 12, 2026

### What We Discussed

**Goal:** Generate high-quality brand images for ads using AI

**Options evaluated:**
1. ✅ **Nano Banana 2 (Google Imagen)** - Cloud API
   - Installed skill: `/Users/userclaw/.openclaw/workspace/skills/nano-banana-2-skill/`
   - Excellent text rendering (perfect for ads with text)
   - Two provider options:
     - Atlas Cloud: $0.056-$0.072/image (flat-rate)
     - Google AI Studio: $0.067-$0.151/image (scales with resolution)
   - **Status:** Skill installed, NO API KEY SET YET

2. ✅ **Stable Diffusion 3.5 Large** - Local generation
   - Latest flagship model from Stability AI
   - 8B parameters, excellent quality
   - Best for: text rendering, prompt adherence, final ad assets
   - **Hardware:** M2 Mac with 16GB RAM can run it (slower but works)
   - **Speed:** ~60-120 seconds per image
   - **Setup needed:** ComfyUI + model download from Hugging Face

### Hardware Specs
- **System:** Mac mini (M2 chip, Apple Silicon)
- **RAM:** ~16GB unified memory
- **GPU:** Apple Metal (no NVIDIA CUDA)
- **Can run:** SDXL, SD 3.5 Large (slower than NVIDIA but works)

### Recommended Approach (Hybrid)

**Phase 1: Quick Start (Cloud)**
- Get API key (Atlas Cloud or Google AI Studio)
- Use Nano Banana 2 for immediate results
- Generate 20-30 test images (~$1-$3 total)
- Dial in brand style quickly

**Phase 2: Local Setup (Free Forever)**
- Install ComfyUI (open-source workflow tool)
- Download SDXL first (faster, test workflows)
- Add SD 3.5 Large for final high-quality assets
- Zero per-image costs, unlimited generations

### Why Both?
- **Cloud:** Fast results today, test concepts quickly
- **Local:** Free unlimited use, full control, no ongoing costs

## Next Steps (When Resuming)

**To pick up where we left off, say:**
> "Let's work on brand images"

**Then choose a path:**

### Path A: Cloud (Fast Start)
1. Pick provider: Atlas Cloud or Google AI Studio
2. Get API key
3. Set environment variable
4. Generate first brand images

### Path B: Local (Free Forever)
1. Install ComfyUI
2. Download Stable Diffusion models
3. Set up workflows
4. Generate images locally

### Path C: Both (Recommended)
1. Start with cloud for quick testing (Path A)
2. Set up local generation while testing (Path B)
3. Use cloud for speed, local for volume

## Key Files
- Nano Banana skill: `/Users/userclaw/.openclaw/workspace/skills/nano-banana-2-skill/SKILL.md`
- Output folder: TBD (create when generating)

## Resources
- **Atlas Cloud:** https://www.atlascloud.ai
- **Google AI Studio:** https://aistudio.google.com/apikey
- **Draw Things (Mac app):** https://drawthings.ai
- **ComfyUI (local):** https://github.com/comfyanonymous/ComfyUI
- **SD 3.5 Large model:** https://huggingface.co/stabilityai/stable-diffusion-3.5-large

## Blockers
None - ready to start whenever you are

## Session Continuity Notes

**For next session:**
- Read this STATUS.md file
- Nano Banana 2 skill already installed
- M2 Mac hardware confirmed compatible
- Need to decide: cloud (fast) vs local (free) or both

---

**🎨 Ready to generate brand images!**  
Next: Choose your path and start creating.
