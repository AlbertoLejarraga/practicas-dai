from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from mi_aplicacion.models import Libro, Autor, Prestamo, Usuario

class formAddLibro(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ('isbn', 'titulo', 'autor', 'imagen')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Guardar libro'))
class formCrearAutor(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ('nombre', 'apellidos')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Guardar autor'))

class formCrearUsuario(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('dni', 'nombre', 'apellidos', 'tipo', 'email')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Guardar usuario'))
    def dniReadonly(self):
        self.fields['dni'].widget.attrs["readonly"] = True

class formPrestamo(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ('fecha', 'duracion_dias', 'usuario', 'libro', 'estado')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Guardar préstamo'))
    def setLibroInicial(self, pk):
        self.fields['libro'].initial = pk
    def paraClientes(self):
        self.fields["fecha"].widget.attrs["readonly"] = True
        self.fields["duracion_dias"].widget.attrs["readonly"] = True
        self.fields["estado"].widget.attrs["readonly"] = True
        self.fields.pop('usuario')
