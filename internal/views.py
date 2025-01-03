from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from sales.models import Telecaller


class EditTelecallerView(View):
    template_name = "internal/edit_telecaller.html"

    def get(self, request, t_id):
        # Fetch the telecaller instance
        telecaller = get_object_or_404(Telecaller, id=t_id)
        return render(request, self.template_name, {"telecaller": telecaller})

    def post(self, request, t_id):
        # Fetch the telecaller instance
        telecaller = get_object_or_404(Telecaller, id=t_id)

        # Update the telecaller instance with the new data
        telecaller.name = request.POST.get("name")
        telecaller.role = request.POST.get("role")
        telecaller.max_leads = request.POST.get("max_leads")
        telecaller.save()

        return redirect("edit-telecaller", t_id=telecaller.id)