import importlib.util, re
spec = importlib.util.spec_from_file_location('g','gen_cv_typ.py')
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

def show(label, jd):
    print('==', label)
    print('  keywords:', g._jd_highlight_keywords(jd))

SAMPLE_JD = (
    'Senior Business/Functional Analyst (Data Platform Transformation) - Freelance '
    'Healthcare Sector\n\n'
    'We are looking for a Senior Business/Functional Analyst with strong Data '
    'expertise to drive our data platform transformation initiative.\n\n'
    'Responsibilities:\n'
    '  - Analyse data requirements, identify data gaps, and implement data '
    'integration.\n'
    "  - Participate in data migration from legacy systems to the new data platform.\n"
    'Profile:\n'
    "  - 5 years' experience as a Business/Functional Analyst\n"
    '  - Good understanding of Data Platforms, Integrations\n'
)
show('SAMPLE_JD', SAMPLE_JD)

# Now test the actual JD file
with open('job_descriptions/CV-20260920-0013.txt', encoding='utf-8') as f:
    real_jd = f.read()
show('real JD', real_jd)

# Now test highlighting
src = open('gen_cv_typ.py', encoding='utf-8').read()
start = src.index('    cv1_body = (\n') + len('    cv1_body = (\n')
end = src.index('\n    transform(', start)
body = src[start:end]
highlighted = g.highlight_jd(body, SAMPLE_JD)
print('\n-- highlighting (SAMPLE_JD) --')
for block in re.split(r'#entry\(', highlighted)[1:]:
    combs = re.findall(r'\"([^\"]*)\",', block)
    cname = combs[1] if len(combs)>=2 else '?'
    print('  GREY' if 'important: true' in block else '  norm', cname)
