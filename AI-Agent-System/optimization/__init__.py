"""
Optimization module for disaster resource allocation.

This module provides mathematical optimization models using linear/integer programming
to allocate volunteers and resources across disaster zones optimally.
"""

from .volunteer_allocator import VolunteerAllocator, run_allocation

__all__ = ['VolunteerAllocator', 'run_allocation']
