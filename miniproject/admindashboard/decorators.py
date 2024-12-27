# from django.shortcuts import redirect
# from django.urls import reverse

# def admin_restricted(view_func):
#     """
#     A decorator to restrict admin users from accessing certain views.
#     """
#     def _wrapped_view(request, *args, **kwargs):
#         if request.user.is_staff or request.user.is_superuser:
#             return redirect(reverse('admindashboard:admin_dashboard'))  # Redirect admins to their dashboard
#         return view_func(request, *args, **kwargs)
#     return _wrapped_view
