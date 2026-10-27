import os
import re
import ast
from pathlib import Path

STOP_WORDS = {'the', 'system', 'shall', 'user', 'allow', 'must', 'should', 'provide', 'support', 'with', 'from', 'that', 'this', 'for', 'and', 'are'}

class ProjectAnalyzer:
    @staticmethod
    def scan_files(extracted_path):
        """
        Recursively scans directory for text & python source files.
        Returns a dictionary { relative_file_path: file_content }
        """
        source_files = {}
        if not os.path.exists(extracted_path):
            return source_files

        ignore_dirs = {'venv', 'env', '.git', '__pycache__', '.pytest_cache', 'migrations', 'staticfiles', 'uploads'}

        for root, dirs, files in os.walk(extracted_path):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            for file in files:
                _, ext = os.path.splitext(file.lower())
                if ext in ['.py', '.html', '.css', '.js', '.md', '.txt', '.json', '.sh', '.yml', '.yaml', '.csv']:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, extracted_path).replace('\\', '/')
                    try:
                        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                            source_files[rel_path] = f.read()
                    except Exception:
                        pass
        return source_files

    @staticmethod
    def inspect_python_code(source_files):
        """
        Inspects python files for AST definitions (classes, functions, imports, docstrings).
        """
        py_files = {path: content for path, content in source_files.items() if path.endswith('.py')}
        classes = []
        functions = []
        lines_of_code = 0
        has_tests = False
        test_files = []
        has_readme = any('readme' in p.lower() for p in source_files.keys())

        for rel_path, content in py_files.items():
            lines = content.splitlines()
            lines_of_code += len(lines)

            if 'test' in rel_path.lower() or os.path.basename(rel_path).startswith('test_'):
                has_tests = True
                test_files.append(rel_path)

            try:
                tree = ast.parse(content, filename=rel_path)
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        classes.append({'name': node.name, 'file': rel_path, 'line': node.lineno})
                    elif isinstance(node, ast.FunctionDef):
                        functions.append({'name': node.name, 'file': rel_path, 'line': node.lineno, 'args': [a.arg for a in node.args.args]})
            except SyntaxError:
                # Fallback to regex parsing if AST fails
                for i, line in enumerate(lines, 1):
                    cls_match = re.search(r'class\s+([A-Za-z0-9_]+)', line)
                    if cls_match:
                        classes.append({'name': cls_match.group(1), 'file': rel_path, 'line': i})
                    fn_match = re.search(r'def\s+([A-Za-z0-9_]+)', line)
                    if fn_match:
                        functions.append({'name': fn_match.group(1), 'file': rel_path, 'line': i})

        return {
            'py_files_count': len(py_files),
            'total_lines_of_code': lines_of_code,
            'classes': classes,
            'functions': functions,
            'has_tests': has_tests or any('/tests/' in p or p.startswith('tests/') for p in source_files.keys()),
            'test_files_count': len(test_files),
            'has_readme': has_readme
        }


class RequirementMatcher:
    @staticmethod
    def extract_keywords(req_description):
        words = re.findall(r'[a-zA-Z0-9_]+', req_description.lower())
        keywords = [w for w in words if len(w) > 2 and w not in STOP_WORDS]
        return keywords

    @staticmethod
    def match_requirement(req, source_files, py_inspection):
        """
        Matches requirement description against python files, classes, functions, and line content.
        Returns dict with status, evidence_file, evidence_function, description, suggestion, priority.
        """
        keywords = RequirementMatcher.extract_keywords(req.description)
        if not keywords:
            keywords = [req.category.lower()]

        matched_files = []
        matched_functions = []
        matches_count = 0

        # 1. Search in class & function names
        for fn in py_inspection.get('functions', []):
            fn_name = fn['name'].lower()
            if any(kw in fn_name for kw in keywords):
                matched_functions.append(f"{fn['name']} ({fn['file']}:L{fn['line']})")
                if fn['file'] not in matched_files:
                    matched_files.append(fn['file'])
                matches_count += 2

        for cls in py_inspection.get('classes', []):
            cls_name = cls['name'].lower()
            if any(kw in cls_name for kw in keywords):
                matched_functions.append(f"Class {cls['name']} ({cls['file']}:L{cls['line']})")
                if cls['file'] not in matched_files:
                    matched_files.append(cls['file'])
                matches_count += 2

        # 2. Search in raw file content
        for rel_path, content in source_files.items():
            content_lower = content.lower()
            file_match_score = sum(1 for kw in keywords if kw in content_lower)
            if file_match_score >= 1:
                if rel_path not in matched_files:
                    matched_files.append(rel_path)
                matches_count += file_match_score

        # SRS Rule logic
        if matches_count >= 3 or len(matched_functions) >= 1:
            status = 'Implemented'
            suggestion = 'Maintain clean separation of concerns and ensure full unit test coverage.'
        elif matches_count >= 1 or len(matched_files) >= 1:
            status = 'Partial'
            suggestion = f'Requirement is partially implemented. Check {matched_files[0] if matched_files else "source code"} to complete implementation.'
        else:
            status = 'Missing'
            suggestion = f'No implementation evidence found for keywords: {", ".join(keywords[:5])}. Consider adding appropriate module/function.'

        evidence_file = matched_files[0] if matched_files else 'N/A'
        evidence_function = matched_functions[0] if matched_functions else 'N/A'

        return {
            'status': status,
            'evidence_file': evidence_file,
            'evidence_function': evidence_function,
            'description': f"Requirement [{req.requirement_id}] '{req.description}' matched {matches_count} evidence keyword(s).",
            'suggestion': suggestion,
            'priority': req.priority
        }


class QualityChecker:
    @staticmethod
    def check_quality(source_files, py_inspection):
        """
        Runs code quality rules:
        - Long functions (> 35 lines)
        - snake_case naming for Python functions
        - Exception handling (try/except)
        - Hardcoded secret / password pattern
        - README documentation
        """
        findings = []
        passed_rules = 0
        total_rules = 5

        # Rule 1: Function Length
        py_files = {p: c for p, c in source_files.items() if p.endswith('.py')}
        long_fns = []
        for p, content in py_files.items():
            lines = content.splitlines()
            current_fn = None
            fn_len = 0
            for line in lines:
                if line.strip().startswith('def '):
                    if current_fn and fn_len > 35:
                        long_fns.append((current_fn, p, fn_len))
                    current_fn = line.strip().split('(')[0].replace('def ', '')
                    fn_len = 1
                elif current_fn:
                    fn_len += 1
            if current_fn and fn_len > 35:
                long_fns.append((current_fn, p, fn_len))

        if long_fns:
            fn_desc = ", ".join([f"{name} ({length} lines)" for name, path, length in long_fns[:3]])
            findings.append({
                'category': 'Quality',
                'title': 'Long Function Warning',
                'status': 'Partial',
                'evidence_file': long_fns[0][1],
                'evidence_function': long_fns[0][0],
                'description': f"Found {len(long_fns)} function(s) exceeding 35 lines limit: {fn_desc}.",
                'suggestion': 'Refactor long functions into smaller, modular helper functions.',
                'priority': 'Medium'
            })
        else:
            passed_rules += 1

        # Rule 2: Function Naming (snake_case)
        non_snake = []
        for fn in py_inspection.get('functions', []):
            name = fn['name']
            if not name.startswith('__') and not re.match(r'^[a-z_][a-z0-9_]*$', name):
                non_snake.append(f"{name} ({fn['file']})")

        if non_snake:
            findings.append({
                'category': 'Quality',
                'title': 'Naming Convention Deviation',
                'status': 'Partial',
                'evidence_file': py_inspection.get('functions', [{}])[0].get('file', 'N/A'),
                'evidence_function': non_snake[0],
                'description': f"Found functions not following PEP8 snake_case: {', '.join(non_snake[:3])}.",
                'suggestion': 'Rename function identifiers to use snake_case for standard Python styling.',
                'priority': 'Low'
            })
        else:
            passed_rules += 1

        # Rule 3: Exception Handling
        has_try_except = any('try:' in content and 'except' in content for content in py_files.values())
        if has_try_except:
            passed_rules += 1
        else:
            findings.append({
                'category': 'Quality',
                'title': 'Missing Exception Handling',
                'status': 'Partial',
                'evidence_file': list(py_files.keys())[0] if py_files else 'N/A',
                'evidence_function': 'N/A',
                'description': 'No try/except error handling blocks detected in Python files.',
                'suggestion': 'Add proper try/except exception handling around file I/O, database, and network operations.',
                'priority': 'Medium'
            })

        # Rule 4: Hardcoded Password / Secret Pattern
        hardcoded_secrets = []
        secret_pattern = re.compile(r'(password|secret|api_key|token)\s*=\s*[\'"][^\'"]+[\'"]', re.IGNORECASE)
        for p, content in py_files.items():
            for line_no, line in enumerate(content.splitlines(), 1):
                if secret_pattern.search(line) and 'django-insecure' not in line:
                    hardcoded_secrets.append(f"{p}:L{line_no}")

        if hardcoded_secrets:
            findings.append({
                'category': 'Quality',
                'title': 'Hardcoded Secret / Password Detected',
                'status': 'Missing',
                'evidence_file': hardcoded_secrets[0],
                'evidence_function': 'N/A',
                'description': f"Potential hardcoded credentials found in: {', '.join(hardcoded_secrets[:3])}.",
                'suggestion': 'Extract sensitive configuration into environment variables or secrets file.',
                'priority': 'High'
            })
        else:
            passed_rules += 1

        # Rule 5: README Documentation
        if py_inspection.get('has_readme'):
            passed_rules += 1
        else:
            findings.append({
                'category': 'Documentation',
                'title': 'Missing README Documentation',
                'status': 'Missing',
                'evidence_file': 'README.md',
                'evidence_function': 'N/A',
                'description': 'No README.md or project documentation file was detected in project root.',
                'suggestion': 'Add a clear README.md file explaining project features, installation, and usage instructions.',
                'priority': 'Medium'
            })

        quality_score = round((passed_rules / total_rules) * 100, 1)

        return quality_score, findings


class ScoreCalculator:
    @staticmethod
    def calculate(req_findings, quality_score, py_inspection):
        """
        SRS Section 18:
        Status Scores: Implemented=1.0, Partial=0.5, Missing=0.0, Manual Review=0.25
        Compliance Score = (Total Requirement Score / Number of Requirements) * 100
        Overall Score = Compliance * 0.60 + Code Quality * 0.20 + Testing * 0.10 + Documentation * 0.10
        """
        if not req_findings:
            compliance_score = 100.0
        else:
            status_map = {'Implemented': 1.0, 'Partial': 0.5, 'Missing': 0.0, 'Manual Review': 0.25}
            total_req_score = sum(status_map.get(f.current_status if hasattr(f, 'current_status') else f.status, 0.0) for f in req_findings)
            compliance_score = (total_req_score / len(req_findings)) * 100.0

        # Testing score calculation
        if py_inspection.get('has_tests'):
            testing_score = min(100.0, 50.0 + (py_inspection.get('test_files_count', 1) * 25.0))
        else:
            testing_score = 0.0

        # Documentation score calculation
        doc_score = 100.0 if py_inspection.get('has_readme') else 40.0

        # SRS Formula: Overall Score = Compliance * 0.60 + Quality * 0.20 + Testing * 0.10 + Doc * 0.10
        overall = (compliance_score * 0.60) + (quality_score * 0.20) + (testing_score * 0.10) + (doc_score * 0.10)

        return {
            'compliance_score': round(compliance_score, 1),
            'quality_score': round(quality_score, 1),
            'testing_score': round(testing_score, 1),
            'doc_score': round(doc_score, 1),
            'overall_score': int(round(overall))
        }
