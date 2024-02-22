"""
PyTuneSmith: A Python library for creating and manipulating music.

This library provides tools for generating musical compositions, applying audio effects, and synthesizing audio from musical scores.
"""

# Import the core functionality into the package namespace
from .core import Effect, InstrumentTrack, LyricsTrack, Song
from .effects import ConvolutionEffect, GainEffect
from .effects.effects_pack import EffectsPack

# Define the package version
__version__ = "0.1.4"
