{
    'name': 'Hospital Management System',
    'version': '1.0',
    'author': 'Kerollos Samy',
    'summary': 'Manage patients, doctors, appointments, and medical records in a hospital.',
    'description': """This module provides a comprehensive Hospital Management System (HMS) for managing various aspects of a hospital, including patients, doctors, appointments, and medical records. It includes features such as patient registration, appointment scheduling, medical history tracking, and billing.""",
    'depends': ['base'],
    'data': [
        'views/menu.xml',
        'views/patient.xml',
        'security/ir.model.access.csv',
    ],
    'application': True,
    'installable': True,
}
