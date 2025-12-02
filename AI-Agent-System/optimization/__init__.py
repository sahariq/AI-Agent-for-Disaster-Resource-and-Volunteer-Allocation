"""
Optimization module for disaster resource allocation.

This module provides mathematical optimization models using linear/integer programming
to allocate volunteers and resources across disaster zones optimally.
"""

from .volunteer_allocator import VolunteerAllocator

__all__ = ['VolunteerAllocator']
